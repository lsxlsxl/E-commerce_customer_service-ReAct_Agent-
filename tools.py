import sqlite3


# 计算表达式
def calculate(operation: str) -> float:
    return eval(operation)


# 根据产品名称查询产品的数据信息
def query_by_product_name(product_name):
    # 连接 SQLite 数据库
    conn = sqlite3.connect('SportsEquipment.db')
    cursor = conn.cursor()

    # 使用SQL查询按名称查找产品。'%'符号允许部分匹配。
    cursor.execute("SELECT * FROM products WHERE product_name LIKE ?", ('%' + product_name + '%',))

    # 获取所有查询到的数据
    rows = cursor.fetchall()
    
    # 关闭连接
    conn.close()

    return rows


# 读取目前的优惠政策
def read_store_promotions(product_name):
    try:
        file_path = 'store_promotions.txt'

        with open(file_path, 'r', encoding='utf-8') as file:
            promotions_content = file.readlines()

        # 搜索包含产品名称的行
        filtered_content = [line for line in promotions_content if product_name in line]

        # 返回匹配的行，如果没有找到，返回一个默认消息
        if filtered_content:
            return ''.join(filtered_content)
        else:
            return "No favorable policies for this product were found."
        
    except FileNotFoundError:
        # 文件不存在的错误处理
        return "The preferential policy document was not found. Please check if the file path is correct."
    
    except Exception as e:
        # 其他潜在错误的处理
        return f"An error occurred while reading the preferential policy document:{str(e)}"
    

if __name__ == "__main__":
    # 功能测试

    # 1.计算
    print('计算功能测试：')
    print(calculate("120 * 0.9"))

    # 2. 查询
    print('查询功能测试：')
    matching_products = query_by_product_name('球')
    print("Matching Products:")
    for product in matching_products:
        print(product)

    # 3.读取
    print('查询功能测试：')
    result = read_store_promotions('篮球')
    print(result.strip())