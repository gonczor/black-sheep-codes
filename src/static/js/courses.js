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
        async getCourseDetails(x){
            const courseId = x.target.dataset.id;
            const response = await axios.get(
                '/api/v1/courses/' + courseId +'/',
                {
                    headers: {
                        Authorization: 'Token ' + window.localStorage.token
                    }
                }
            );
            this.courseDetails = response.data;
        }
    },
    data() {
        return {
            courses: [],
            courseDetails: {}
        }
    },
    mounted() {
        this.listCourses();
    }
}

Vue.createApp(HelloVueApp).mount('#courses-list');
