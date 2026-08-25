# ウェーブレット特徴量画像対応データセットテンプレート

## 概要
材料観察画像（SEM/TEM像や相の分布画像）などパターン画像（模様やテクスチャなど）に対して、ウェーブレット変換のひとつであるSteerable Pyramids手法によりマルチスケールな特徴や構造の抽出を行えます。

- tifフォーマットの画像ファイルを入力する
- 代表画像は入力ファイルをpng化したもの
- MultiDataTile対応（１つの送り状で複数のデータ登録を行う）


## メタ情報
- [メタ情報](docs/requirement_analysis/要件定義.xlsx)

## 基本情報

### データ登録方法
- 送り状画面をひらいて入力ファイルに関する情報を入力する
- 「登録ファイル」欄に登録したいファイルをドラッグアンドドロップする。
  - 登録したいファイルのフォーマットは、\*.tif、\*.tiff の何れか一つとなります。
  - 複数のファイルを入力し一度に複数のデータを登録することが可能。
  - 複数のファイルを入力する場合は、「データ名」に「${filename}」と入力し「データ名」に入力ファイル名をマッピングさせることができる
- 「登録開始」ボタンを押して（確認画面経由で）登録を開始する

## 構成

### レポジトリ構成

```
wavelet_transform_characterization
├── README.md
├── benchmark
│   ├── __init__.py
│   ├── target_benchmark_script.py
│   └── typecheck_mypy_pyrefly_benchmark.py
├── container
│   ├── Dockerfile
│   ├── Dockerfile_nims (NIMSイントラ用)
│   ├── data (入出力(下記参照))
│   ├── main.py
│   ├── modules (ソースコード)
│   │   ├── __init__.py
│   │   ├── datasets_process.py
│   │   ├── graph_handler.py
│   │   ├── inputfile_handler.py
│   │   ├── interfaces.py
│   │   ├── invoice_handler.py
│   │   ├── meta_handler.py
│   │   ├── structured_handler.py
│   │   └── wavelet.py
│   ├── pip.conf
│   ├── pyproject.toml
│   ├── requirements-test.txt
│   ├── requirements.txt
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── fixtures
│   │   │   └── template_files.py
│   │   ├── test_meta.py
│   │   └── test_output.py
│   └── tox.ini
├── docs (ドキュメント)
│   ├── manual (マニュアル)
│   ├── mkdoc_ci_scripts.py
│   ├── requirement_analysis
│   │   └── 要件定義.xlsx
│   └── template
│       └── README.md
├── inputdata (サンプルデータ)
│   ├── test1
│   │   ├── inputdata
│   │   │   └── QPAF-C5.tif
│   │   └── invoice
│   │       └── invoice.json
│   ├── test2
│   │   ├── inputdata
│   │   │   └── QPAF-C5_test.tiff
│   │   └── invoice
│   │       └── invoice.json
│   └── test3
│       ├── inputdata
│       │   ├── QPAF-C5.tif
│       │   └── QPAF-C5_test.tiff
│       └── invoice
│           └── invoice.json
└── templates (テンプレート群)
     └── template
         ├── batch.yaml
         ├── catalog.schema.json
         ├── invoice.schema.json
         ├── jobs.template.yaml
         ├── metadata-def.json
         └── tasksupport
             ├── invoice.schema.json
             ├── metadata-def.json
             └── rdeconfig.yaml
```

### 動作環境ファイル入出力

```
│   ├── container/data
│   │   ├── attachment
│   │   ├── inputdata
│   │   │   └── 登録ファイル欄にドラッグアンドドロップした任意のファイル
│   │   ├── invoice
│   │   │   └── invoice.json (送り状ファイル)
│   │   ├── main_image
│   │   │   └── (メイン)入力画像をpng化した画像
│   │   ├── meta
│   │   │   └── metadata.json (主要パラメータメタ情報ファイル)
│   │   ├── nonshared_raw
│   │   │   └── inputdataからコピーした入力ファイル
│   │   ├── other_image
│   │   ├── structured
│   │   │   └── steerable_pyramid_feature.csv (ウェーブレット特徴量ファイル)
│   │   ├── tasksupport (テンプレート群)
│   │   │   ├── invoice.schema.json
│   │   │   ├── metadata-def.json
│   │   │   └── rdeconfig.yaml
│   │   └── thumbnail
│   │       └── (サムネイル用)プロット画像
```

## データ閲覧
- データ一覧画面を開く。
- ギャラリー表示タブでは１データがタイル状に並べられている。データ名をクリックして詳細を閲覧する。
- ツリー表示タブではタクソノミーにしたがってデータを階層表示する。データ名をクリックして詳細を閲覧する。

### 動作環境
- Python: 3.13
- RDEToolKit: 1.7.1
