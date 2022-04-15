Vue.createApp({
    data() {
        return {
            loaded: 0,
            LOADED_TARGET: 3,
            data: {},
            ops: {},
            profs: {},
            filter_type: "op"
        }
    },
    computed: {
        filtered_data() {
            if (this.loaded < this.LOADED_TARGET) { return {}; }
            var data = {};
            for (var key in this.data) {
                var item = this.data[key];
                if (
                    this.filter_type=="op" && this.ops[item['op']].show ||
                    this.filter_type=="prof" && this.profs[item['prof']].sub[item['subprof']].show
                ) { data[key] = this.data[key]; }
            }
            return data;
        }
    },
    mounted () {
        this.loadData(this.data, 'data/data.json');
        this.loadData(this.ops, 'data/ops.json');
        this.loadData(this.profs, 'data/profs.json');
    },
    methods: {
        loadData: function(target, url) {
            console.log('load data from ' + url);
            axios.get(url)
                .then(response => {
                    for (var key in response.data) {
                        target[key] = response.data[key];
                    }
                    console.log(target);
                    this.loaded ++;
                    this.setFilter(true);
                })
                .catch(function (error) { console.log(error); });
        },
        setFilter: function(s) {
            for (var key in this.ops) {
                this.ops[key].show = s;
            }
            for (var key in this.profs) {
                for (var skey in this.profs[key].sub) {
                    this.profs[key].sub[skey].show = s;
                }
            }
        }
    }
}).mount('#app')