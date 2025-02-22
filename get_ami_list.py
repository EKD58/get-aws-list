import boto3
import csv

# ACCESS_KEYとSECRET_KEYを入力してください
ACCESS_KEY = 'ACCESSKEY'
SECRET_KEY = 'SECRETKEY'
REGION_NAME = 'ap-northeast-1'

# AMIの一覧を取得する
def get_ami_list():
    # AWSの認証情報を設定する
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )
    
    # EC2クライアントを作成する
    ec2_client = session.client('ec2')
    
    # 自分のアカウントのAMIの情報を取得する
    response = ec2_client.describe_images(Owners=['self'])
    
    ami_list = []
    
    for image in response['Images']:
        #print(image)
        print(image.get('ImageId', 'N/A'))

        ami_id = image.get('ImageId', 'N/A')
        ami_name = image.get('Name', 'N/A')
        ami_state = image.get('State', 'N/A')
        ami_creation_date = image.get('CreationDate', 'N/A')
        ami_architecture = image.get('Architecture', 'N/A')
        ami_platform = image.get('PlatformDetails', 'N/A')
        ami_description = image.get('Description', 'N/A')
        ami_owner_id = image.get('OwnerId', 'N/A')
        ami_tags = image.get('Tags', [])

        ami_tag_name = ''
        for tag in ami_tags:
            if tag['Key'] == 'Name':
                ami_tag_name = tag['Value']
                break

        ami_list.append([ami_id, ami_name, ami_tag_name, ami_state, ami_creation_date, ami_architecture, ami_platform, ami_description, ami_owner_id])

    # AMI名でソートする
    ami_list.sort(key=lambda x: x[1])

    return ami_list

# 取得した情報をCSVファイルに出力する
def write_ami_to_csv(ami_list):
    with open('ami_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AMI ID', 'AMI 名', 'タグ名', 'ステータス', '作成日時', 'アーキテクチャ', 'プラットフォーム', '説明', 'オーナーID'])
        
        for ami in ami_list:
            writer.writerow(ami)

# AMIの一覧を取得する
ami_list = get_ami_list()

# 取得した情報をCSVファイルに出力する
write_ami_to_csv(ami_list)
