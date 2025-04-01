def separate_think_answer(response):
    think = response.split('<think>')[1].split('</think>')[0]
    answer = response.split('</think>')[1]
    return think, answer

def save_temp_file(temp_file_path, uploaded_file):
    file_content = uploaded_file.read()
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)