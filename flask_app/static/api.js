const calendarApp = new Vue({
    el: '#calendar',
    data: {
        // デフォルトは全国
        PrefectureCode: "00",
        items: [],
        options: []
    },
    mounted: function () {
        // デフォルト(東京)のカレンダーを表示
        this.setCalendar();
        // 選択肢に東京以外の都道府県を表示
        this.setPrefectures();
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
        // セレクトボックスの地域を変更した際に発火
        changePrefecture: function (event) {
            this.PrefectureCode = event.target.value;
            this.setCalendar();
        }
    }
})
