new Vue({
    el: '#app',
    data: {
      columns: ['Index', 'Last Name', 'First Name', 'Age', 'Job', 'Address', 'Actions '],
      persons: [{
        lname: "ADIASSA",
        fname: "Ethiel",
        age: 20,
        job: "Web Developer",
        address: "Lome-Togo"
      }, {
        lname: "ADUFU",
        fname: "Patrick",
        age: 20,
        job: "Banker",
        address: "Senegal-Dakar"
      }, {
        lname: "MOUTON",
        fname: "John",
        age: 28,
        job: "Scientist",
        address: "New-York/USA"
      }, {
        lname: "SMITH",
        fname: "Luther",
        age: 18,
        job: "Pilot",
        address: "London/GB"
      }, {
        lname: "WALTER",
        fname: "Ramses Peter",
        age: 38,
        job: "Doctor",
        address: "Paris/France"
      }, {
        lname: "GEORGES",
        fname: "Luther",
        age: 45,
        job: "Musician",
        address: "Vienne"
      }, {
        lname: "MICHAEL",
        fname: "Daven",
        age: 27,
        job: "Boxer",
        address: "Pekin/China"
      }],
      bin: [],
      input: {
        lname: "WADE",
        fname: "Johnson",
        age: 38,
        job: "Comedian",
        address: "Roma/Italia"
      },
      editInput: {
        lname: "",
        fname: "",
        age: 0,
        job: "",
        address: ""
      }
    },
    methods: {
      //function to add data to table
      add: function() {
        this.persons.push({
          lname: this.input.lname,
          fname: this.input.fname,
          age: this.input.age,
          job: this.input.job,
          address: this.input.address
        });
  
        for (var key in this.input) {
          this.input[key] = '';
        }
        this.persons.sort(ordonner);
        this.$refs.lname.focus();
      },
      //function to handle data edition
      edit: function(index) {
        this.editInput = this.persons[index];
        console.log(this.editInput);
        this.persons.splice(index, 1);
      },
      //function to send data to bin
      archive: function(index) {
        this.bin.push(this.persons[index]);
        this.persons.splice(index, 1);
        this.bin.sort(ordonner);
      },
      //function to restore data
      restore: function(index) {
        this.persons.push(this.bin[index]);
        this.bin.splice(index, 1);
        this.bin.sort(ordonner);
      },
      //function to update data
      update: function(){
        // this.persons.push(this.editInput);
         this.persons.push({
          lname: this.editInput.lname,
          fname: this.editInput.fname,
          age: this.editInput.age,
          job: this.editInput.job,
          address: this.editInput.address
        });
         for (var key in this.editInput) {
          this.editInput[key] = '';
        }
        this.persons.sort(ordonner);
      },
      //function to defintely delete data 
      deplete: function(index) {
        // console.log(this.bin[index]);
        this.bin.splice(index, 1);
      }
    }
  });
  
  //function to sort table data alphabetically
  var ordonner = function(a, b) {
    return (a.lname > b.lname);
  };
  
  $(function() {
    //initialize modal box with jquery
    $('.modal').modal();
  });