import csv
from django.core.management.base import BaseCommand
from comparator.models import FontFeature

class Command(BaseCommand):
    help = 'CSVファイルからフォント特徴量をインポートします'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='インポートするCSVファイルのパス')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        
        # 既存のデータをクリア
        FontFeature.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('既存の特徴量データをクリアしました。'))

        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            features_to_create = []
            for row in reader:
                feature = FontFeature(
                    font_name=row['font_name'],
                    character=row['character'],
                    vector=row['vector']
                )
                features_to_create.append(feature)
        
        # bulk_createで高速にDBへ保存
        FontFeature.objects.bulk_create(features_to_create)

        self.stdout.write(self.style.SUCCESS(f'{len(features_to_create)}件のデータをインポートしました。'))