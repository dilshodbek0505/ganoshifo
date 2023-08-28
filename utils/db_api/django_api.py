import requests as r

url = "http://127.0.0.1:8000/"

class Database:
    async def get_category():
        """
        Barcha katgoriyalarni olish
        """
        res = r.get(f"{url}category/")
        return res.json()
    async def get_product(category = None, id = None):
        if category:
            res = r.get(f"{url}product/?category_id__name={category}")
        if id:
            res = r.get(f"{url}product/?category_id__name=&id={id}")

        return res.json()
    async def set_member(full_name, telegram_id, user_name = None):
        data = {
            "full_name": full_name,
            "telegram_id": telegram_id,
            "user_name": user_name
        }
        res = r.post(f"{url}/member/", data=data)
        return res.json()
    async def get_about():
        req = r.get(f"{url}about/")
        return req.json()
    async def set_client(product, first_name, last_name, phone, city, address):
        data = {
            "product_id": product,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "city": city,
            "address": address
        }
        req = r.post(f"{url}client/", data=data)
        return req.json()
    
    async def get_member():
        res = r.get(f"{url}member/")
        return res.json() 

    async def  get_lesson():
        res = r.get(f"{url}lesson/")
        return res.json()
    
    async def get_lesson_next(url_1):
        res = r.get(url_1)
        return res.json()
    
    async def get_one_lesson(pk):
        res = r.get(f"{url}lesson/{pk}/")
        return res.json()