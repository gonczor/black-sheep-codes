const HelloVueApp = {
    el: '#vueApp',
    methods: {
        async listCourses(){
            const response = await axios.get(
                '/api/v1/courses/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.courses = response.data.results;
            await this.listOwnCourses();
        },
        async listOwnCourses(){
            const ownCoursesResponse = await axios.get(
                '/api/v1/courses/list-assigned/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.ownCourses = ownCoursesResponse.data.results;
        },
        async getCourseDetails(event){
            const courseId = event.target.dataset.id;
            const response = await axios.get(
                '/api/v1/courses/' + courseId + '/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.courseDetails = response.data;
            this.displaySignup = true;
        },
        async signUpForCourse() {
            const courseId = this.courseDetails.id;
            try {
                const response = await axios.post(
                    '/api/v1/course-signups/',
                    {
                        course: courseId
                    },
                    {
                        headers: {
                            Authorization: 'Token ' + window.localStorage.token
                        },
                    }
                );
                if(response.status === 201) {
                    this.showSuccessfulSignupToast();
                    await this.listOwnCourses();
                }
            } catch (error) {
                let message = "";
                if (error.response.data.nonFieldErrors === undefined){
                    message = error.response.data.detail
                } else {
                     message = error.response.data.nonFieldErrors.join('\n');
                }
                alert(message);
            }

        },
        hasDetails() {
            return this.displaySignup;
        },
        showSuccessfulSignupToast() {
            this.signupToast.className = "show";
            setTimeout(
        function(){
                    this.signupToast.className = this.signupToast.className.replace("show", "");
                },
                3000
            );

        },
    },
    data() {
        return {
            courses: [],
            ownCourses: [],
            courseDetails: {},
            displaySignup: false,
            signupToast: document.getElementById('signupToast')
        }
    },
    mounted() {
        this.listCourses();
    }
}

const app = Vue.createApp(HelloVueApp)
app.config.errorHandler = (error, vm, info) => {
    console.log(error);
};
app.mount('#courses-list');
