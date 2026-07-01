# Phân tích lỗi API Create sản phẩm:

# 1. Client gửi yêu cầu:
#    POST /products
#    Kèm dữ liệu sản phẩm mới.
# 2. FastAPI nhận dữ liệu và tạo đối tượng
#    ProductCreate từ request body.
# 3. Hàm create_product() được thực thi.
# 4. Chương trình tạo ngay new_product
#    mà không kiểm tra mã sản phẩm (code)
#    đã tồn tại hay chưa.
# 5. Sản phẩm mới được thêm vào danh sách
#    bằng products.append(new_product).
# 6. API luôn trả về:
#    "Create product successfully"
#    dù mã sản phẩm bị trùng.


# Vì sao bị lỗi:
# - Không kiểm tra trùng mã sản phẩm trước khi thêm.
# - Có thể tạo nhiều sản phẩm cùng một code.
# - Dữ liệu bị trùng, gây khó khăn khi quản lý,
#   tìm kiếm và cập nhật sản phẩm.
# - API cũng chưa trả về HTTP 201 Created
#   khi tạo thành công.


# Test case chứng minh lỗi:

# Test 1:
# Gửi:
# code = "SP001"
# Kết quả hiện tại:
# Tạo thành công.
# Kết quả đúng:
# Báo lỗi mã sản phẩm đã tồn tại.

# Test 2:
# Gửi:
# code = "SP002"
# Kết quả hiện tại:
# Tạo thành công.
# Kết quả đúng:
# Báo lỗi mã sản phẩm đã tồn tại.

# Sửa lại code


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    for item in products:
        if item["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail="Mã sản phẩm đã tồn tại"
            )

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }