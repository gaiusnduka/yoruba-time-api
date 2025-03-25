from gtts import gTTS  # Google Text-to-Speech
import datetime
import os

# Yoruba Numbers (Simplified for Pronunciation)
yoruba_numbers = {
    1: "kan", 2: "meji", 3: "meta", 4: "merin", 5: "marun",
    6: "mefa", 7: "meje", 8: "mejo", 9: "mesan", 10: "mewa",
    11: "mokunla", 12: "mejila", 13: "metala", 14: "merinla", 15: "medogun",
    16: "merindilogun", 17: "metadilogun", 18: "mejidilogun", 19: "mokandilogun", 20: "ogun",
    21: "meedogbon", 22: "mejilelogun", 23: "metetalelogun", 24: "merinlelogun", 25: "marunlelogun",
    26: "mefilelogun", 27: "mejelelogun", 28: "mejolelogun", 29: "mesanlelogun", 30: "abo",
    31: "metadinlogbon", 32: "mejidinlogbon", 33: "metadinlogbon", 34: "merindinlogbon", 35: "marundinlogbon",
    36: "mefadinlogbon", 37: "mejedinlogbon", 38: "mejodinlogbon", 39: "mesandinlogbon", 40: "ogbon",
    41: "metadinlogorin", 42: "mejidinlogorin", 43: "metadinlogorin", 44: "merindinlogorin", 45: "medogun", 
    46: "mefadinlogorin", 47: "mejedinlogorin", 48: "mejodinlogorin", 49: "mesandinlogorin", 50: "aadota",
    51: "metadinlaadota", 52: "mejidinlaadota", 53: "metadinlaadota", 54: "merindinlaadota", 55: "marundinlaadota",
    56: "mefadinlaadota", 57: "mejedinlaadota", 58: "mejodinlaadota", 59: "mesandinlaadota"
}

# Function to translate English time to Yoruba
def translate_time_to_yoruba(time_str):
    try:
        time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        return "Invalid time format. Use format: '3:45 PM'"

    hour = time_obj.hour
    minute = time_obj.minute
    period = "AM" if hour < 12 else "PM"

    # Fix for 12:00 AM (midnight)
    hour = 12 if hour == 0 else (hour if hour <= 12 else hour - 12)
    yoruba_hour = yoruba_numbers[hour]

    # Convert minutes
    if minute == 0:
        yoruba_minute = ""
    elif minute == 15:
        yoruba_minute = f"ati iseju {yoruba_numbers[15]}"  
    elif minute == 30:
        yoruba_minute = f"ati iseju {yoruba_numbers[30]}"  
    elif minute == 45:
        yoruba_minute = f"ku iseju merindilogun"
        yoruba_hour = yoruba_numbers[(hour % 12) + 1]
    elif minute < 30:
        yoruba_minute = f"ati iseju {yoruba_numbers[minute]}"
    else:
        remaining = 60 - minute
        yoruba_hour = yoruba_numbers[(hour % 12) + 1]
        yoruba_minute = f"ku iseju {yoruba_numbers[remaining]}"

    # Determine time of day
    time_of_day = "owuro" if period == "AM" else "osan" if 12 <= hour < 19 else "oru"

    # Final Yoruba time sentence
    yoruba_time = f"Aago {yoruba_hour} {yoruba_minute} {time_of_day}".strip()
    return yoruba_time

# Function to convert time and play Yoruba speech
def speak_time_in_yoruba(time_str):
    yoruba_text = translate_time_to_yoruba(time_str)

    if "Invalid time format" in yoruba_text:
        print(yoruba_text)
        return  

    print(f"English Time: {time_str}")
    print(f"Yoruba Time: {yoruba_text}")

    try:
        # Convert Yoruba text to speech (Use "en" because "yo" is not supported)
        tts = gTTS(yoruba_text, lang="yo")  # Force Yoruba phonetics
        tts.save("yoruba_time.mp3")

        print("Playing Yoruba time audio...")
        os.system("start yoruba_time.mp3" if os.name == "nt" else "afplay yoruba_time.mp3")

    except Exception as e:
        print("⚠️ Warning: Unable to generate voice output. (Check your internet connection)")
        print("Error details:", str(e))  # Prints error for debugging

# Main execution
if __name__ == "__main__":
    user_time = input("Enter time (e.g., 3:45 PM): ")  
    speak_time_in_yoruba(user_time)
    
    # Keep console open
    input("\nPress Enter to exit...")
