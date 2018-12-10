from telegram import ReplyKeyboardMarkup


REDIS_COLLECTION_NAME = 'tg_test_bot'  # data is stored here

NAME, AGE, GENDER, CITY, COUNTRY = 'name', 'age', 'gender', 'city', 'country'
FIELDS = (NAME, AGE, GENDER, CITY, COUNTRY)

# age is chosen from predefined options
AGE_OPTIONS = [['male', 'female', 'other']]
GENDER_REPLY_MARKUP = ReplyKeyboardMarkup(AGE_OPTIONS, one_time_keyboard=True)
CHOICE_FIELDS = {
    GENDER: GENDER_REPLY_MARKUP
}

# non str field types should be specified here
FIELD_TYPES = {
    AGE: int
}
