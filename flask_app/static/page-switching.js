const PageSwitchingApp = new Vue({
    el: '#left-navi',
    data: {
        isCalenderActive: true,
    },
    methods: {
        showCalender() {
            this.isCalenderActive = true;
        },
    },
});
