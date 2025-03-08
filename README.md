---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


# 1. Giới thiệu về dự án Quản lý tài sản
Dự án này nhằm mục đích quản lý tài sản của một tổ chức, trong đó có các thực thể chính như Loại tài sản, Tài sản cụ thể, Đơn mượn & trả tài sản; cung cấp các chức năng sau:
* Quản lý loại tài sản
* Quản lý tài sản cụ thể
* Phân bổ tài sản cho các phòng ban
* Khấu hao tài sản
* Kiểm kê tài sản
* Luân chuyển tài sản
* Thanh lý tài sản
* Quản lý đơn mượn tài sản & cấp phát tài sản
![Loại tài sản](./images/loai-tai-san.png)
![Tài sản cụ thể](./images/tai-san-cu-the.png)
![Phân bổ tài sản](./images/phan-bo-tai-san.png)
![Khấu hao tài sản](./images/khau-hao-tai-san.png)
![Kiểm kê tài sản](./images/kiem-ke-tai-san.png)
![Luân chuyển tài sản](./images/luan-chuyen-tai-san.png)
![Thanh lý tài sản](./images/thanh-ly-tai-san.png)
![Quản lý mượn tài sản](./images/don-muon-tai-san.png)
![Quản lý cấp phát tài sản](./images/cap-phat-tai-san.png)

# 2. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 2.1. Clone project.

```
git clone https://github.com/nguyenngocdantruong/TTDN-15-04-N6.git
git checkout 
```

## 2.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 2.3. khởi tạo môi trường ảo.

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
python3.10 -m venv ./venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

# 3. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo apt install docker-compose
```
```
sudo docker-compose up -d
```

# 4. Setup tham số chạy cho hệ thống

## 4.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

# 5. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```


Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
    
