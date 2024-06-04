Vue.component("modal", {
    template: "#modal-template"
});

var app = new Vue({
    el: "#app",

    data: {
        serviceURL: "https://cs3103.cs.unb.ca:8006",
        authenticated: false,
        personalList: null,
        usersList: null,
        userPresents:null,
        editModal: false,
        addPresent: false,
        presentData: null,
        userInfo: null,
        loggedIn: null,
        input: {
            username: "",
            password: "",
            Quantity: 1,
            user_id: ""
        },
        present:{
            list: "",
            user_id: "",
            present_id: "",
            quantity: ""
        }
    },
    
    mounted: function() {
        axios
        .get(this.serviceURL+"/login")
        .then(response => {
          if (response.data.status == "success") {
            this.authenticated = true;
            this.loggedIn = response.data.user_id;
          }
        })
        .catch(error => {
            this.authenticated = false;
            console.log(error);
        });
    },

    methods:{
        login(){
            if (this.input.username != "" && this.input.password != "") {
                axios
                .post(this.serviceURL+"/login", {
                    "username": this.input.username,
                    "password": this.input.password
                })
                .then(response => {
                    if (response.data.status == "success") {
                      this.authenticated = true;
                      this.loggedIn = response.data.user_id;
                    }
                })
                .catch(e => {
                    alert("Incorrect username or password");
                    this.input.password = "";
                    console.log(e);
                });
            } else {
                alert("Please Enter a username and a password");
            }
        },
        
        
        logout(){
            axios
            .delete(this.serviceURL+"/login")
            .then(response => {
                location.reload();
                this.authenticated=false;
            })
            .catch(e => {
                console.log(e);
            });
        },


        showList(){
            axios
            .get(this.serviceURL+"/myList")
            .then(response => {
                this.personalList = response.data.presents;
                this.presentData = null;
                this.usersList=null;
                this.userPresents=null;
            })
            .catch(e => {
                alert("Unable to load the List data")
                console.log(e);
            });
        },

        updateQuantity(presentId){
            this.showModal();
            for(x in this.personalList){
                if(this.personalList[x].present_ID == presentId){
                    this.present = this.personalList[x];
                    this.present.present_id = this.personalList[x].present_ID;
                    break;
                }
            }
        },

        update(){
            axios
            .put(this.serviceURL+"/myList/" + this.present.present_id, {
                "Quantity": this.present.quantity
            })
            .then(response => {
                this.hideModal();
                alert("Successfully updated the quantity");
            })
            .catch(e => {
                alert("Unable to update quantity");
                console.log(e);
                console.log(this.present.present_id);
            });
        },

        showModal(){
            this.editModal = true;
        },

        hideModal() {
            this.editModal = false;
            this.addPresent = false;
        },

        removePresentFromList(presentId){
            axios
            .delete(this.serviceURL+"/myList/"+presentId)
            .then(response =>  {
                this.showList();
                alert("Successfully deleted present from list");
             })
             .catch(e => {
                alert("Unable to remove present from list");
                console.log(e);
           });
        },

        getPresents(){
            axios
            .get(this.serviceURL+"/presents")
            .then(response => {
                this.presentData = response.data.presents;
                this.personalList = null;
                this.usersList=null;
                this.userPresents=null;
                console.log("In get Presents" + this.presentData[0].cost);
            })
            .catch(e => {
                alert("Unable to retrieve presents");
                console.log(e);
            });
        },

        showAdd(){
            this.addPresent = true;
        },

        add(present_id){
            this.showAdd();
            for(x in this.presentData){
                if(this.presentData[x].present_id == present_id){
                    this.present = this.presentData[x];
                    break;
                }
            }
        },

        addPresentToList(){
            axios
            .post(this.serviceURL+"/presents/"+ this.present.present_id, {
                "Quantity": this.present.quantity
            })
            .then(response => {
                alert("Successfully added to list");
                this.hideModal();
            })
            .catch(e => {
                alert("Oops, something happened");
            })
        },


        getUsers(){
            axios
            .get(this.serviceURL+"/users")
            .then(response => {
                this.usersList = response.data.User;
                this.personalList=null;
                this.presentData=null;
                this.userPresents=null;
            })
            .catch(e => {
                alert("Something went wrong when retrieving a list of users");
            })
        },

        getUserList(userId){
            axios
            .get(this.serviceURL+"/users/" + userId + "/presents/")
            .then(response => {
                this.userInfo = response.data.User;
                this.userPresents = response.data.present;
                this.personalList = null;
                this.presentData = null;
            })
            .catch(e => {
                alert("Error retrieving user's list");
            })
        }
    }
});

