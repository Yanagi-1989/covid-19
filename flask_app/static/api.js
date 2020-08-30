const calendarApp = new Vue({
    el: '#calendar',
    // jinja2のデリミタ {{}} と競合するため、デリミタを変更
    delimiters: ["[[", "]]"],
    data: {
        // デフォルトは東京
        PrefectureCode: "13",
        items: [],
        options: []
    },
    mounted: function () {
        this.setPrefectures();
        this.setCalendar();
    },
    methods: {
        setCalendar: function () {
            axios.get('/calendar/' + this.PrefectureCode)
                .then(response => {
                    this.items = response.data;
                }).catch(error => {});
        },
        setPrefectures: function () {
            axios.get('/prefectures')
                .then(response => {
                    this.options = response.data;
                }).catch(error => {});
        },
        changePrefecture: function (event) {
            this.PrefectureCode = event.target.value;
            this.setCalendar();
        }
    }
})
