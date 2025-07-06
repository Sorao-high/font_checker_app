from django.shortcuts import render
from .forms import ComparisonForm
from .models import FontFeature
import numpy as np
import cv2
from skimage.feature import hog
from skimage.transform import resize
from numpy.linalg import norm

# Colabで設定したHOGパラメータと全く同じものを定義
IMAGE_SIZE = (128, 128)
HOG_PIXELS_PER_CELL = (16, 16)
HOG_CELLS_PER_BLOCK = (2, 2)

def preprocess_user_image(image_file):
    """アップロードされた画像の前処理とHOG特徴量抽出"""
    # 1. 画像を読み込み、グレースケールに変換
    image_bytes = image_file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img_gray = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    # 2. 二値化（背景を白、文字を黒に）
    # 大津の二値化を使い、背景が明るいことを想定して反転(THRESH_BINARY_INV)
    _ , img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. 輪郭を見つけて最大のものを切り出す
    contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("画像から文字を検出できませんでした。輪郭のはっきりした画像をアップロードしてください。")
        
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    char_img = img_thresh[y:y+h, x:x+w]

    # 4. 正方形の背景に中央配置し、リサイズ
    max_dim = max(w, h)
    top_pad = (max_dim - h) // 2; bottom_pad = max_dim - h - top_pad
    left_pad = (max_dim - w) // 2; right_pad = max_dim - w - left_pad
    padded_img = cv2.copyMakeBorder(char_img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0) # 背景は黒
    resized_img = cv2.resize(padded_img, IMAGE_SIZE, interpolation=cv2.INTER_AREA)

    # 5. HOG特徴量を抽出
    # scikit-imageのhogは黒背景・白オブジェクトを期待するので、resized_imgをそのまま使う
    fd = hog(resized_img, orientations=8, pixels_per_cell=HOG_PIXELS_PER_CELL,
             cells_per_block=HOG_CELLS_PER_BLOCK, visualize=False, feature_vector=True)
    return fd

def cosine_similarity(vec_a, vec_b):
    """コサイン類似度を計算する"""
    if norm(vec_a) == 0 or norm(vec_b) == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))

def main_view(request):
    form = ComparisonForm()
    context = {'form': form}

    if request.method == 'POST':
        form = ComparisonForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                font_name = form.cleaned_data['font_name']
                character = form.cleaned_data['character']
                user_image = form.cleaned_data['image']

                base_feature = FontFeature.objects.get(font_name=font_name, character=character)
                base_vector = base_feature.get_vector_as_numpy()

                user_vector = preprocess_user_image(user_image)
                
                similarity = cosine_similarity(base_vector, user_vector)
                score = max(0, similarity) * 100

                context['result'] = {
                    'score': f"{score:.1f}",
                    'font_name': font_name,
                    'character': character,
                }
            except Exception as e:
                context['error'] = f'処理中にエラーが発生しました: {e}'
        else:
            context['error'] = 'フォームの入力内容が正しくありません。'

    return render(request, 'comparator/main.html', context)