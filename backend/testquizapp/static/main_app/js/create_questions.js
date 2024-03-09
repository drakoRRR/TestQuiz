function addQuestion() {
    let questionHtml = '<div class="question mb-3">' +
        '<label for="questionText">Question:</label>' +
        '<input type="text" class="form-control" name="questions[]" required>' +
        '<div class="file-input-wrapper mt-2">' +
        '<label for="questionImage" class="btn btn-outline-primary">Upload Image</label>' +
        '<input type="file" id="questionImage" name="questionImages[]" accept="image/*" onchange="displayFileName(this)">' +
        '<span class="file-input-text"></span>' +
        '</div>' +
        '<label for="questionType" class="mt-2">Question Type:</label>' +
        '<select class="form-control" name="questionTypes[]">' +
        '<option value="free">Вільна відповідь</option>' +
        '<option value="single">Одна правильна відповідь</option>' +
        '<option value="multiple">Декілька правильних відповідей</option>' +
        '</select>' +
        '<button type="button" class="btn btn-info mt-2 add-answer-btn" onclick="addAnswer(this)">Add Answer</button>' +
        '<div class="answersContainer mt-2"></div>' +
        '</div>';

    $('#questionsContainer').append(questionHtml);
}

function addAnswer(button) {
    let answerHtml = '<div class="answer">' +
        '<label for="answerText">Answer:</label>' +
        '<input type="text" class="form-control" name="answers[]" required>' +
        '<div class="file-input-wrapper mt-2">' +
        '<label for="answerImage" class="btn btn-outline-primary">Upload Image</label>' +
        '<input type="file" id="answerImage" name="answerImages[]" accept="image/*" onchange="displayFileName(this)">' +
        '<span class="file-input-text"></span>' +
        '</div>' +
        '<div class="form-check mt-2">' +
        '<input type="checkbox" class="form-check-input" name="isCorrect">' +
        '<label class="form-check-label" for="isCorrect">Correct Answer</label>' +
        '</div>' +
        '</div>';

    $(button).siblings('.answersContainer').append(answerHtml);
}

function displayFileName(input) {
    let fileName = input.files[0].name;
    $(input).siblings('.file-input-text').text(fileName);
}

function collectFormData() {
    let questions = [];
    let len_questions = 0;
    $('.question').each(function () {
        let question = {};
        len_questions++;
        question['question_name'] = $(this).find('input[name="questions[]"]').val();

        let questionImageInput = $(this).find('input[name="questionImages[]"]')[0];
        let questionImageFile = questionImageInput.files[0];
        question['question_image'] = questionImageFile;

        question['question_type'] = $(this).find('select[name="questionTypes[]"]').val();
        question['is_free_answer'] = question['question_type'] === 'free';
        question['is_only_one_correct_answer'] = question['question_type'] === 'single';
        question['is_few_correct_answers'] = question['question_type'] === 'multiple';
        question['question_choices'] = [];

        $(this).find('.answer').each(function () {
            let answer = {};
            answer['choice_name'] = $(this).find('input[name="answers[]"]').val();
            answer['is_correct'] = $(this).find('input[name="isCorrect"]').is(':checked');

            let answerImageInput = $(this).find('input[name="answerImages[]"]')[0];
            let answerImageFile = answerImageInput.files[0];
            answer['choice_image'] = answerImageFile;

            question['question_choices'].push(answer);
        });
        question['len_question_choices'] = question['question_choices'].length;

        questions.push(question);
    });

    let currentURL = window.location.href;
    let url = new URL(currentURL);
    let test_id = url.searchParams.get("test_id");

    let formData = new FormData();
    formData.append('test_id', test_id);
    formData.append('questions_amount', len_questions.toString())

    questions.forEach((question, index) => {
        formData.append(`question_name[${index}]`, question['question_name']);
        formData.append(`question_image[${index}]`, question['question_image']);
        formData.append(`question_type[${index}]`, question['question_type']);
        formData.append(`is_free_answer[${index}]`, question['is_free_answer']);
        formData.append(`is_only_one_correct_answer[${index}]`, question['is_only_one_correct_answer']);
        formData.append(`is_few_correct_answers[${index}]`, question['is_few_correct_answers']);
        formData.append(`len_question_choices[${index}]`, question['len_question_choices']);

        question['question_choices'].forEach((choice, choiceIndex) => {
            formData.append(`questions[${index}]choice_name[${choiceIndex}]`, choice['choice_name']);
            formData.append(`questions[${index}]is_correct[${choiceIndex}]`, choice['is_correct']);
            formData.append(`questions[${index}]choice_image[${choiceIndex}]`, choice['choice_image']);
        });
    });

    $.ajax({
        url: '/api-create-question/',
        type: 'POST',
        headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.error('AJAX Error:', error);
        }
    });
}
