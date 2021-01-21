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
            this.courses = response.data;
        },
    },
    data() {
        return {
            courses: []
        }
    },
    mounted() {
        this.listCourses();
    }
}

Vue.createApp(HelloVueApp).mount('#courses-list');
