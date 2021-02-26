const CourseDetailsApp = {
    methods: {
        async fillSectionsList(){
             const sectionsList = await axios.get(
                '/api/v1/courses/' + this.courseId +'/retrieve-assigned/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.sections = sectionsList.data.sections;
        },
        async getLessonDetails(event){
            this.lessonId = event.target.dataset.lessonId;
            const response = await axios.get(
                '/api/v1/lessons/' + this.lessonId + '/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.lessonDetails = response.data;
            if(this.isTest()){
                this.setupTest()
            }
        },
        setupTest(){
            this.testQuestionIndex = 0;
            this.testQuestions = [];
            if(this.lessonDetails.questions === undefined){
                return;
            }
            this.lessonDetails.questions.forEach((value, index, array) => {
                this.testQuestions.push({
                    text: value.text,
                    answers: value.answers,
                    markedCorrect: false
                });
                if(this.lessonDetails.questions.length > 0){
                    this.setCurrentTestQuestion();
                }
            });
        },
        async markLessonAsComplete(){
            await axios.post(
                '/api/v1/lessons/' + this.lessonId + '/mark-as-complete/',
                {},
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.lessonDetails.isComplete = true;
            await this.fillSectionsList();
        },
        async revertMarkLessonAsComplete(){
            await axios.post(
                '/api/v1/lessons/' + this.lessonId + '/revert-mark-as-complete/',
                {},
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.lessonDetails.isComplete = false;
            await this.fillSectionsList();
        },
        isLesson(){
            if (this.lessonDetails === null){
                return false
            }
            return this.lessonDetails.lessonType.toLowerCase() === "lesson";
        },
        isTest(){
            if (this.lessonDetails === null){
                return false
            }
            return this.lessonDetails.lessonType.toLowerCase() === "test";
        },
        getCorrectAnswersCounter() {
            let correctAnswers = 0;
            this.testQuestions.forEach((value, index, array) => {
                if (value.markedCorrect)
                    correctAnswers++;
            });
            return correctAnswers + '/' + this.testQuestions.length;
        },
        checkAnswer(event){
            const correctAnswers = this.currentTestQuestion.answers.filter((answer) => {
                return answer.isCorrect
            });
            const correctId = correctAnswers.map((answer) => {return answer.id})[0];
            if (this.selectedAnswerId !== null && Number(this.selectedAnswerId) === correctId){
                this.currentTestQuestion.markedCorrect = true;
            } else {
                this.currentTestQuestion.markedCorrect = false;
                if(this.selectedAnswerId !== null ){
                    let answerLabel = document.getElementById('answer-' + this.selectedAnswerId);
                    answerLabel.classList.add('incorrect-answer');
                }
            }
            let correctAnswerLabel = document.getElementById('answer-' + correctId);
            correctAnswerLabel.classList.add('correct-answer');
        },
        selectAnswer(event){
            this.selectedAnswerId = event.target.id;
        },
        moveToNextQuestion(){
            if (this.testQuestionIndex < this.testQuestions.length)
                this.testQuestionIndex++;
            if(!this.isBeyondLastQuestion())
                this.setCurrentTestQuestion();
        },
        moveToPreviousQuestion() {
            if(this.testQuestionIndex > 1)
                this.testQuestionIndex--;
            this.setCurrentTestQuestion();
        },
        setCurrentTestQuestion() {
            this.currentTestQuestion = this.testQuestions[this.testQuestionIndex];
        },
        isBeyondLastQuestion() {
            return this.testQuestionIndex === this.testQuestions.length;
        }
    },
    data() {
        return {
            courseId: null,
            sections: [],
            lessonDetails: null,
            lessonId: null,
            testQuestionIndex: 0,
            testQuestions: [],
            currentTestQuestion: null,
            selectedAnswerId: null
        }
    },
    mounted() {
        this.courseId = window.location.pathname.split('/').slice(-2)[0];
        this.fillSectionsList().then();
    }
};

const app = Vue.createApp(CourseDetailsApp);
app.config.errorHandler = (error, vm, info) => {
    console.log(error);
};
app.mount('#app');
