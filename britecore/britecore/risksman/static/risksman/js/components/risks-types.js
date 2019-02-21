const RiskTypes = {
    data() {
        return {
            fields: [],
            risksTypes: [],
            newRiskType: {
                title: null,
                opts: []
            },
            opt: '',
            loading: false
            
        }
    },

    mounted() {
        this.getFields();
        this.getRisksTypes();
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
        
        getRisksTypes() {
            this.loading = true;
            this.$http.get('/api/v1/risks-types/').then(
                
               success => {
                   this.risksTypes = success.body;
                   this.loading = false;
                   console.log('Success: ', success);
               },
                
               error => {
                   this.loading = false;
                   console.log('Error: getRisksTypes()', error);
            }
         );
        },


        addRiskType(){
            this.loading = true;
            this.$http.post('/api/v1/risks-types/', this.newRiskType).then(
                
                success => {
                    this.loading = false;
                    console.log('Success: ', success);
                    this.getRisksTypes();
                    $('#newRiskType').modal('hide');
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: addRiskType()', error);
                }


            );

        },
        

        deleteRiskType(id){
            this.loading = true;
            this.$http.delete(`/api/v1/risks-types/${id}/`).then(
                
                success => {
                    this.loading = false;
                    console.log('Success: ', success);
                    this.getRisksTypes();
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: deleteFieldType()', error);
                }

            );
        },

        getFieldName(id){
            for (f of this.fields){
                if (f.id == id){
                    return f.title;
                }
            }
            return `Field: #${id}`;
        }
         
    },
    
    props: [],

    template: `
   <main>
   <template v-if="risksTypes.length > 0">
   <div class="table-responsive">
    <table class="table">
       <thead>
         <tr>
         <th>#</th>
         <th>Title</th>
         <th>Fields</th>
         <th>Actions</th>
         </tr>
       </thead>
       <tbody>
       
        <tr v-for="f of risksTypes">
          <th>{{ f.id }}</th>
          <td>{{ f.title }}</td>
          <td>
            <span 
             class="badge badge-secondary mx-1"
             v-for="opt of f.opts">
               {{ getFieldName(opt) }}
            </span>
          </td>
          <td>
              <button class="btn btn-danger py-0" @click="deleteRiskType(f.id)">Delete</button>
         </td>
       </tr>
       </tbody>
    </table>
 </div>
    <button class="btn btn-primary mt-2 px-5" data-toggle="modal" data-target="#newRiskType">Add More</button>
   </template>


    <div v-else-if="fields.length == 0" class="text-center">

      <h4>:( No Fields detected.</h4>
     <span class="badge badge-info">Tip</span>
     
      <br>
   
       <button type="button" 
            class="btn btn-primary mt-2 px-5" 
            @click="$router.push('/')">
       Add New Field
      </button>
    </div>

    <div v-else class="text-center">

      <h4>:( No Risks Type yet.</h4>

      <br>
   
    <button class="btn btn-primary mt-2 px-5" data-toggle="modal" data-target="#newRiskType">Add New</button>
    </div>


<div class="modal fade" id="newRiskType" tabindex="-1" role="dialog" aria-labelledby="newRiskTypeModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="newRiskTypeModalLabel">
        Add New Field
        </h5>

        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form v-on:submit.prevent="addRiskType()">
      <div class="modal-body">
          <div class="form-group">
                <label for="field-title">Title</label>
                      <input v-model="newRiskType.title"
                        type="text"
                        class="form-control"
                        id="field-title"
                        placeholder="Enter Field Title" 
                        required>
                    </div>
                    <div class="form-group">
                      <label for="field-widget">Fields</label>
                      <select v-model="newRiskType.opts" 
                         class="form-control"
                        id="field-widget"
                        multiple
                        required>
                        <option v-for="f in fields" :value="f.id">
                         {{ f.title }}
                        </option>
                         </select>
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
<div class="loading bg-secondary text-white px-4 py-1" v-show="loading">Loading ..</div>
   </main>
    `

}


Vue.component('risk-types', RiskTypes);
