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
        }
    },
    data() {
        return {
            courseId: null,
            sections: [],
            lessonDetails: null,
            lessonId: null
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
