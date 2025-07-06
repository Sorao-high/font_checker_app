# font_checker_app
手書き文字が、特定のお手本フォントとどれだけ似ているかを判定するWebアプリケーション
![image](https://github.com/user-attachments/assets/43c1d436-1002-4a10-b612-a72e40795962)


## 概要

これは、あなたの手書き文字が、特定のお手本フォントとどれだけ似ているかを判定するWebアプリケーションです。
紙に書いた文字を写真に撮ってアップロードするだけで、手書き文字の特徴量と、お手本フォントの特徴量との類似度をパーセンテージで表示します。

このプロジェクトは、PythonのWebフレームワーク**Django**をバックエンドに、**OpenCV**と**scikit-image**を利用した画像処理・パターン認識技術を組み合わせて構築されています。

## 主な機能

- **フォントとお手本の選択**: データベースに登録されているフォント（例: 明朝体）と文字を選択します。
- **画像アップロード**: 手書きした文字を撮影した画像をアップロードします。
- **類似度判定**: アップロードされた画像から文字の形状特徴（HOG特徴量）を抽出し、お手本フォントの特徴量と比較。コサイン類似度を用いてそっくり度を計算します。
- **結果表示**: 判定結果をパーセンテージで分かりやすく表示します。

## 使用技術

- **バックエンド**: Django
- **画像処理**: OpenCV, scikit-image, Pillow
- **フロントエンド**: HTML, CSS (Bootstrap 5)
- **データベース**: SQLite3 (デフォルト)

## セットアップと実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
Use code with caution.
Markdown
2. 仮想環境の作成と有効化 (推奨)
Generated bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
Use code with caution.
Bash
3. 必要なライブラリのインストール
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
(注: requirements.txtが存在しない場合は、以下のコマンドで手動インストールしてください)
Generated bash
pip install django numpy opencv-python-headless scikit-image Pillow
Use code with caution.
Bash
4. データベースの初期設定
お手本フォントの特徴量データをデータベースにインポートします。
（リポジトリにfont_features.csvが含まれていることを確認してください）
Generated bash
# データベースのマイグレーション
python manage.py migrate

# CSVから特徴量データをインポート
python manage.py import_features font_features.csv
Use code with caution.
Bash
5. 開発サーバーの起動
Generated bash
python manage.py runserver
Use code with caution.
Bash
ブラウザで http://127.0.0.1:8000/ にアクセスすると、アプリケーションが表示されます。

新しいフォントの追加方法
このアプリケーションは拡張性があり、自分で好きなお手本フォントを追加することができます。
フォントの追加は、付属のGoogle Colabノートブックを使用して行います。
手順
フォントファイルの準備:
追加したいフォントのファイル（.ttfまたは.ttc形式）を用意します。
Google Colabノートブックの実行:
リポジトリ内の generate_features.ipynb (または提供されたColabコード) をGoogle Colaboratoryで開きます。
フォントのアップロードとパスの設定:
用意したフォントファイルをColab環境にアップロードするか、ご自身のGoogle Driveにアップロードします。
ノートブック内のFONT_PATHSセクションで、追加したいフォントの情報を辞書形式で記述します。キーにフォント名、値にフォントファイルのパスを指定してください。
Generated python
# 例: ゴシック体を追加する場合
FONT_PATHS = {
    'Mincho': '/path/to/Mincho.ttc',  # 既存のフォント
    'Gothic': '/path/to/your_gothic.ttf'  # 新しく追加するフォント
}
Use code with caution.
Python
特徴量の生成:
ノートブックのセルを上から順に実行します。処理が完了すると、新しいフォントの特徴量が含まれたfont_features.csvファイルが生成され、自動的にダウンロードされます。
データベースの更新:
ダウンロードした新しいfont_features.csvファイルで、プロジェクト内の古いファイルを上書きします。
ターミナルで以下のコマンドを実行し、データベースを新しいデータで更新します。
Generated bash
python manage.py import_features font_features.csv
Use code with caution.
Bash
これで、アプリケーションのドロップダウンリストに新しいフォントが追加され、判定に利用できるようになります。
