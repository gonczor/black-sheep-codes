const HelloVueApp = {
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
        },
        async getCourseDetails(event){
            const courseId = event.target.dataset.id;
            const response = await axios.get(
                '/api/v1/courses/' + courseId +'/',
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
                console.log(response);
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
        }
    },
    data() {
        return {
            courses: [],
            courseDetails: {},
            displaySignup: false,
        }
    },
    mounted() {
        this.listCourses();
    }
}

Vue.createApp(HelloVueApp).mount('#courses-list');
