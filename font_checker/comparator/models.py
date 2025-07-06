from django.db import models

# Create your models here.
from django.db import models
import numpy as np

class FontFeature(models.Model):
    font_name = models.CharField(max_length=50)
    character = models.CharField(max_length=10)
    # 特徴量ベクトルは長くなる可能性があるのでTextFieldを使用
    vector = models.TextField()

    class Meta:
        # フォント名と文字の組み合わせはユニーク（重複しない）
        unique_together = ('font_name', 'character')

    def __str__(self):
        return f"{self.font_name} - {self.character}"

    def get_vector_as_numpy(self):
        """保存されている文字列のベクトルをNumpy配列に変換して返す"""
        if not hasattr(self, '_numpy_vector'):
            # 計算結果をキャッシュして毎回変換しないようにする
            self._numpy_vector = np.fromstring(self.vector, sep=',')
        return self._numpy_vector