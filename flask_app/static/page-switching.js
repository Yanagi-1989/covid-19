const PageSwitchingApp = new Vue({
    el: '#left-navi',
    data: {
        isCalenderActive: true,
        isAboutActive: false,
    },
    methods: {
        showCalender() {
            this.isCalenderActive = true;
            this.isAboutActive = false;
        },
        showAbout() {
            this.isCalenderActive = false;
            this.isAboutActive = true;
        },
    },
});
