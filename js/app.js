Vue.createApp({
    data() {
        return {
            ready: false,
            data: {},
            ops: {},
            profs: {},
            filter_type: "op",
            server: "zh_CN",
            server_list: {},
            errormsg: "",
        }
    },
    computed: {
        filtered_data() {
            if (!this.ready) { return {}; }
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
        this.loadData(this.server_list, 'data/server.json');
        this.loadServerData();
    },
    methods: {
        loadServerData: async function() {
            this.clearData()
            if (this.server == "zh_TW") {
                this.errormsg = "[ERROR] zh_TW 暂未实装模组功能"
                return;
            }
            await this.loadData(this.data, 'data/'+this.server+'/data.json');
            await this.loadData(this.ops, 'data/'+this.server+'/ops.json');
            await this.loadData(this.profs, 'data/'+this.server+'/profs.json');
            this.setFilter(true);
            this.ready = true;
        },
        clearData: function() {
            this.ready = false;
            this.data = {};
            this.ops = {};
            this.profs = {};
            this.errormsg = "";
        },
        loadData: function(target, url) {
            console.log('load data from ' + url);
            return new Promise((resolve, reject)=>{
                axios.get(url)
                    .then(response => {
                        for (var key in response.data) {
                            target[key] = response.data[key];
                        }
                        console.log(target);
                        resolve()
                    })
                    .catch(function (error) { console.log(error); reject(); });
            })
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