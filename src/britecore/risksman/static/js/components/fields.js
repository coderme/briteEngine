const Fields = {
    data() {
        return {
            fields: [],
            fieldTypes: [],
            currentField: {},
            newField: {
                id: null,
                title: null,
                widget: null,
                opts: []
            },
            opt: '',
            loading: false
            
        }
    },

    mounted() {
        this.getFieldTypes();
        this.getFields();
    },

    methods: {
        
        getFields() {
            this.loading = true;
            this.$http.get('/api/v1/fields/').then(
                
               success => {
                   this.fields = success.body;
                   this.loading = false;
                   console.log('Success: ', success);
               },
                
               error => {
                   this.loading = false;
                   console.log('Error: getFields()', error);
            }
         );
        },

        addField(){
            this.loading = true;
            this.$http.post('/api/v1/fields/', this.newField).then(
                
                success => {
                    this.loading = false;
                    console.log('Success: ', success);
                    this.getFields();
                    $('#newfield').modal('hide');
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: addField()', error);
                }


            );

        },
        

        deleteField(id){
            this.loading = true;
            this.$http.delete(`/api/v1/fields/${id}/`).then(
                
                success => {
                    this.loading = false;
                    console.log('Success: ', success);
                    this.getFields();
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: deleteField()', error);
                }

            );
        },

        getFieldTypes() {
            this.$http.get('/api/v1/fields-types/').then(
                
                success => {
                    this.fieldTypes = success.body.choices;
                },
                
                error => {
                    console.error('Error: getFieldTypes()', error);
                }
            );
        },

        pushOpt(){
            if (this.opt == '') {
                $('#fieldOpt').focus();
                return;
            }
            this.newField.opts.push({title: this.opt});
            // reset
            this.opt = '';
        },


        deleteOpt(index){
            Vue.delete(this.newField.opts, index);
        },


        editOpt(index, value){
            this.deleteOpt(index);
            this.opt = value;
        }


    },
    
    props: [],

    template: `
   <main>
   <template v-if="fields.length > 0">
   <div class="table-responsive">
    <table class="table">
       <thead>
         <tr>
         <th>#</th>
         <th>Title</th>
         <th>Type</th>
         <th>Options</th>
         <th>Actions</th>
         </tr>
       </thead>
       <tbody>
       
        <tr v-for="f of fields">
          <th>{{ f.id }}</th>
          <td>{{ f.title }}</td>
          <td>{{ f.widget }}</td>
          <td>
            <span 
             class="badge badge-secondary mx-1"
             v-for="opt of f.opts">
               {{ opt.title }}
            </span>
          </td>
          <td>
              <button class="btn btn-danger py-0" @click="deleteField(f.id)">Delete</button>
         </td>
       </tr>
       </tbody>
    </table>
 </div>
    <button class="btn btn-primary mt-2 px-5" data-toggle="modal" data-target="#newfield">Add More</button>
   </template>

    <div v-else class="text-center">

      <h4>:( No Fields yet.</h4>

      <br>
   
    <button class="btn btn-primary mt-2 px-5" data-toggle="modal" data-target="#newfield">Add New</button>
    </div>

<div class="modal fade" id="newfield" tabindex="-1" role="dialog" aria-labelledby="newFieldModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="newFieldModalLabel" v-if="newField.id === null">
        Add New Field
        </h5>
        <h5 class="modal-title" id="newFieldModalLabel" v-else>
        Edit <u>{{ newField.title }}</u>
        </h5>
        


        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form v-on:submit.prevent="addField()">
      <input type="hidden" v-model="newField.id">
      <div class="modal-body">
          <div class="form-group">
                <label for="field-title">Title</label>
                      <input v-model="newField.title"
                        type="text"
                        class="form-control"
                        id="field-title"
                        placeholder="Enter Field Title" 
                        required>
                    </div>
                    <div class="form-group">
                      <label for="field-widget">Type</label>
                      <select v-model="newField.widget" 
                         class="form-control"
                        id="field-widget"
                        required>
                       <option disabled value="">
                       Please select widget
                       </option>
                        <option v-for="f in fieldTypes" :value="f[0]">
                         {{ f[1] }}
                        </option>
                         </select>
                    </div>
                    <div class="form-group" v-show="newField.widget == 'enum'">
                     <label for="fieldOpt">Choices</label>
                     <br>
                     <template v-for="(v, i) of newField.opts">
                        <div class="btn-group" :key="i">
                           <button type="button" 
                              class="btn btn-secondary dropdown-toggle m-1 py-0" 
                              data-toggle="dropdown" 
                              aria-haspopup="true" 
                              aria-expanded="false">
                                  {{ v.title }}
                           </button>
                          <div class="dropdown-menu py-0">
                            <a class="dropdown-item" href="#"
                              @click="editOpt(i, v.title)">
                               Edit
                            </a>
                           <div class="dropdown-divider py-0"></div>
                           <a class="dropdown-item text-danger"
                              href="#" @click="deleteOpt(i)">
                              Delete
                           </a>
                        </div>
                      </div>
                     </template>


                     <div class="form-row align-items-center mx-2">

                      <div class="col-auto">

                       <label class="sr-only" for="fieldOpt">
                         Value
                       </label>

                        <input type="text" v-model.trim="opt"
                           class="form-control mb-2" 
                           id="fieldOpt" placeholder="Apple or Orange">
                      </div>


                      <div class="col-auto">
                           <button type="button" 
                             class="btn btn-success mb-2 "
                              @click="pushOpt()">
                                Add
                           </button>
                      </div>
                    </div>
                    </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary">Save</button>
      </div>
      </form>
    </div>
  </div>
</div>
<div class="loading bg-primary text-white px-4 py-1" v-show="loading">Loading ..</div>
   </main>
    `

}


Vue.component('fields', Fields);
