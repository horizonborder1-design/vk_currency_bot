import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN
from extensions import APIException, CurrencyConverter

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)

GROUP_ID = 238615416
CURRENCIES_RU = ["евро", "доллар", "рубль"]


def send_message(peer_id: int, text: str):
    """Отправляет сообщение пользователю"""
    vk.method("messages.send", {
        "user_id": peer_id,
        "message": text,
        "random_id": random.randint(0, 2**32),
        "group_id": GROUP_ID 
    })


def main():
    print("✅ Бот запущен и ожидает сообщения...")
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.strip().lower()
            peer_id = event.peer_id  

            if text in ["/start", "/help"]:
                send_message(peer_id, "Инструкция...")
                continue
        
            elif text == "/values":
                send_message(peer_id, "Список валют...")
                continue
        
            else:
                try:
                    values = text.split()
                    if len(values) != 3:
                        raise APIException("Введите ровно 3 параметра через пробел.")
                
                    base, quote, amount = values
                    total = CurrencyConverter.get_price(base, quote, amount)
                    send_message(peer_id, f"✅ {amount} {base} = {total} {quote}")
                
                except APIException as e:
                    send_message(peer_id, f"❌ Ошибка: {e}")
                except Exception as e:
                    send_message(peer_id, f"❌ Неизвестная ошибка: {type(e).__name__}")


if __name__ == "__main__":
    main()
