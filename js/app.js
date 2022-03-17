Vue.createApp({
    data() {
        return {
            data: {},
            ops: {}
        }
    },
    computed: {
        filtered_data() {
            var data = {};
            for (var key in this.data) {
                if (this.ops[this.data[key]['op']]['show']) {
                    data[key] = this.data[key];
                }
            }
            return data;
        }
    },
    mounted () {
        this.loadData();
    },
    methods: {
        loadData: function() {
            console.log('load data');
            axios.get("data/data.json")
                .then(response => {
                    this.data = response.data;
                })
                .catch(function (error) { console.log(error); });
            axios.get("data/ops.json")
                .then(response => {
                    for (var key in response.data) {
                        this.ops[key] = {
                            'char': response.data[key]['char'],
                            'name': response.data[key]['name'],
                            'show': true
                        };
                    }
                })
                .catch(function (error) { console.log(error); });
        },
        setFilter: function(s) {
            for (var key in this.ops) {
                this.ops[key]['show'] = s;
            }
        }
    }
}).mount('#app')