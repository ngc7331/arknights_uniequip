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
            progress: [{}, {}],
            progress_key: "arknights_uniequip_progress",
            clear_confirm: 3,
            clear_timeout: null,
        }
    },
    computed: {
        filtered_data() {
            if (!this.ready) { return {}; }
            var data = {};
            for (var key in this.data) {
                var item = this.data[key];
                if (
                    this.filter_type=="op" && this.ops[item["op"]].show ||
                    this.filter_type=="prof" && this.profs[item["prof"]].sub[item["subprof"]].show
                ) { data[key] = this.data[key]; }
            }
            return data;
        }
    },
    mounted () {
        let app = this;
        app.loadData(app.server_list, "data/server.json");
        app.loadServerData();
        app.loadItem(app.progress_key, app.progress);
        window.onbeforeunload = function() {app.saveItem(app.progress_key, app.progress)};
    },
    methods: {
        loadServerData: async function() {
            this.clearData()
            if (this.server == "zh_TW") {
                this.errormsg = "[ERROR] zh_TW 暂未实装模组功能"
                return;
            }
            await this.loadData(this.data, "data/"+this.server+"/data.json");
            await this.loadData(this.ops, "data/"+this.server+"/ops.json");
            await this.loadData(this.profs, "data/"+this.server+"/profs.json");
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
            console.log("load data from " + url);
            return new Promise((resolve, reject)=>{
                axios.get(url)
                    .then(response => {
                        this.copyObject(response.data, target);
                        console.log(target);
                        resolve();
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
        },
        clearProgress: function() {
            let app = this;
            app.clear_confirm --;
            if (app.clear_timeout !== null) {
                clearTimeout(app.clear_timeout);
            }
            if (app.clear_confirm === 0) {
                app.progress = [{}, {}];
                app.clear_confirm = 3;
                clearTimeout(app.clear_timeout);
            }
            app.clear_timeout = setTimeout(function(){app.clear_confirm = 3;}, 2000);
        },
        loadItem: function(key, target) {
            var item = localStorage.getItem(key);
            if (item !== null) {
                this.copyObject(JSON.parse(item), target);
            }
        },
        saveItem: function(key, target) {
            localStorage.setItem(key, JSON.stringify(target));
        },
        copyObject: function(from, to) {
            for (var key in from) {
                to[key] = from[key];
            }
        }
    }
}).mount("#app");