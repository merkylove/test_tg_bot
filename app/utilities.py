from constants import FIELD_TYPES, CHOICE_FIELDS


def merge_step(array1, array2):
    index_array1 = index_array2 = 0

    resulting_array = []

    while index_array1 < len(array1) and index_array2 < len(array2):
        if array1[index_array1] <= array2[index_array2]:
            resulting_array.append(array1[index_array1])
            index_array1 += 1
        else:
            resulting_array.append(array2[index_array2])
            index_array2 += 1

    if index_array1 == len(array1):
        resulting_array.extend(array2[index_array2:])
    else:
        resulting_array.extend(array1[index_array1:])

    return resulting_array


def merge_sort(array):
    middle = len(array) // 2

    if len(array) > 1:

        left_subarray = array[middle:]
        right_subarray = array[:middle]

        left_subarray = merge_sort(left_subarray)
        right_subarray = merge_sort(right_subarray)

        return merge_step(left_subarray, right_subarray)
    else:
        return array


def validate_field(field, value):
    if field in FIELD_TYPES:
        try:
            _ = FIELD_TYPES[field](value)
        except ValueError as e:
            return False

    return True


def generate_question(field_name):
    return 'Enter your {}, please'.format(field_name)


def generate_message(bot, update, field):

    reply_markup = CHOICE_FIELDS.get(field)
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=generate_question(field),
        reply_markup=reply_markup
    )
