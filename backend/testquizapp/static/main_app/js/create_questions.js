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
    var questions = [];
    $('.question').each(function () {
        let question = {};
        question['question_name'] = $(this).find('input[name="questions[]"]').val();
        question['question_image'] = $(this).find('input[name="questionImages[]"]').val();
        question['question_type'] = $(this).find('select[name="questionTypes[]"]').val();
        question['is_free_answer'] = question['question_type'] === 'free';
        question['is_only_one_correct_answer'] = question['question_type'] === 'single';
        question['is_few_correct_answers'] = question['question_type'] === 'multiple';
        question['question_choices'] = [];

        $(this).find('.answer').each(function () {
            let answer = {};
            answer['choice_name'] = $(this).find('input[name="answers[]"]').val();
            answer['is_correct'] = $(this).find('input[name="isCorrect"]').is(':checked');
            answer['choice_image'] = $(this).find('input[name="answerImages[]"]').val();
            question['question_choices'].push(answer);
        });

        questions.push(question);
    });
    console.log(questions)

    let currentURL = window.location.href;
    let url = new URL(currentURL);
    let test_id = url.searchParams.get("test_id");

    $.ajax({
        url: '/api-create-question/',
        type: 'POST',
        headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()},
        data: JSON.stringify({
            'test_id': test_id,
            'questions': questions
        }),
        contentType: 'application/json',
        success: function (response) {
            // Handle the server response here
            console.log(response);
        },
        error: function (error) {
            // Handle any errors that occur during the AJAX request
            console.error('AJAX Error:', error);
        }
    });
}

