import speech_recognition as sr
import pyttsx3
from text2digits import text2digits

class FoodOrderSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.t2d = text2digits.Text2Digits()
        
        # Food menu with prices
        self.menu = {
            "puri": {"price": 25, "description": "Fried Indian bread"},
            "pongal": {"price": 40, "description": "South Indian rice dish"},
            "parotta": {"price": 30, "description": "Layered flatbread"},
            "biryani": {"price": 120, "description": "Fragrant rice dish"},
            "idli": {"price": 35, "description": "Steamed rice cakes"}
        }

    def speak(self, text):
        """Convert text to speech"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen and transcribe speech"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except Exception as e:
                print(f"Error: {e}")
                return None

    def process_order(self, text):
        """Process order and calculate amounts"""
        order = {}
        words = text.split()
        i = 0
        
        while i < len(words):
            word = words[i]
            quantity = 1
            
            # Convert word numbers to digits
            if word.isdigit():
                quantity = int(word)
            else:
                try:
                    quantity = int(self.t2d.convert(word))
                except:
                    pass
            
            # Check if next word is a food item
            if i+1 < len(words) and words[i+1] in self.menu:
                item = words[i+1]
                order[item] = order.get(item, 0) + quantity
                i += 2
            elif word in self.menu:
                order[word] = order.get(word, 0) + 1
                i += 1
            else:
                i += 1
        
        return order

    def generate_bill(self, order):
        """Generate itemized bill"""
        total = 0
        bill_text = "\n=== Your Order ===\n"
        
        for item, qty in order.items():
            price = self.menu[item]["price"]
            item_total = qty * price
            total += item_total
            bill_text += f"{qty} x {item.title()} ({self.menu[item]['description']}): ₹{item_total}\n"
        
        bill_text += f"\nTotal Amount: ₹{total}"
        return bill_text, total

    def run(self):
        """Main system loop"""
        self.speak("Welcome to AI Food Order System. Please speak your order.")
        
        while True:
            text = self.listen()
            
            if not text:
                self.speak("Sorry, I didn't catch that. Please try again.")
                continue
                
            if "exit" in text or "stop" in text:
                self.speak("Thank you for using our service. Goodbye!")
                break
                
            order = self.process_order(text)
            
            if not order:
                self.speak("I didn't recognize any food items. Please try again.")
                continue
                
            bill, total = self.generate_bill(order)
            print(bill)
            
            # Voice response with itemized amounts
            response = "You ordered: "
            for item, qty in order.items():
                price = self.menu[item]["price"]
                response += f"{qty} {item} for {qty*price} rupees, "
            response += f"making total {total} rupees."
            
            self.speak(response)

if __name__ == "__main__":
    system = FoodOrderSystem()
    system.run()