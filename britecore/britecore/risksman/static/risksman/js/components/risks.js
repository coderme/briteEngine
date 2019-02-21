const Risks = {
    data() {
        return {
            risksTypes: [],
            risks: [],
            newRisk : {
                title: null,
                insurer: null,
                risk_type: 0,
                values: []
            },
            risk: 0,
            fields: [],
            loading: false
            
        }
    },

    mounted() {
        this.getRisksTypes();
    },

    methods: {

        getFields(id) {
            this.loading = true;
            this.$http.get(`/api/v1/risks-type-fields/${id}/`).then(
                
               success => {
                   this.fields = success.body.opts;
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




        getRisks(){
            this.loading = true;
            this.$http.get('/api/v1/risks/').then(
                
                success => {
                    this.loading = false;
                    this.risks = success.body;
                    console.log('Success: ', success);
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: getRisks()', error);
                }

            );

        },
        


        addRisk(){
            this.loading = true;
            this.$http.post('/api/v1/risks/', this.newRisk).then(
                
                success => {
                    this.loading = false;
                    console.log('Success: ', success);
                    this.getRisksTypes();
                    $('#newRisk').modal('hide');
                },
                
                error => {
                    this.loading = false;
                    console.log('Error: addRiskType()', error);
                }

            );

        },
        

        deleteRisk(id){
            this.loading = true;
            this.$http.delete(`/api/v1/risks/${id}/`).then(
                
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

        openModalFor(id){
            this.getFields(id);
            $('#newRisk').modal('show');
            this.newRisk.risk_type = id;
        }
        
    },
    
    props: [],

    template: `
   <main>
   <template v-if="risks.length > 0">
   <div class="table-responsive">
    <table class="table">
       <thead>
         <tr>
         <th>#</th>
         <th>Title</th>
         <th>Risk Type</th>
         <th>Insurer</th>
         <th>Data</th>
         <th>Actions</th>
         </tr>
       </thead>
       <tbody>
       
        <tr v-for="f of risks">
          <th>{{ f.id }}</th>
          <td>{{ f.title }}</td>
          <td>{{ f.risk_type.title }}</td>
          <td>{{ f.insurer }}</td>
          <td>
            <table class="table">
             <thead>
              <tr>
               <th>Field</th>
               <th>Value</th>
               </tr>
             </thead>
            <tbody>
              <tr v-for="v of f.values">
               <td>{{ v.field.title }}</td>
               <td>{{ v.value }}</td>
             </tr>
            </tbody>
           </table>
          </td>
          <td>
              <button class="btn btn-danger py-0" 
                   @click="deleteRisk(f.id)">
                 Delete
              </button>
         </td>
       </tr>
       </tbody>
    </table>
 </div>

  </template>


    <div v-else-if="risksTypes.length == 0" class="text-center">

      <h4>:( No Risk Types found.</h4>
     <span class="badge badge-info">Tip</span>
     
      <br>
   
       <button type="button" 
            class="btn btn-primary mt-2 px-5" 
            @click="$router.push('/risks-types/')">
       Add New Field
      </button>
    </div>

    <div v-else class="text-center">

      <h4>No Risks yet :)</h4>
   
    </div>

<form @submit.prevent="openModalFor(risk)">
<div class="form-row" 
     :class="{ 'justify-content-center text-center': risks.length === 0 }">

<div class="col-md-4 col-sm-12">
 <select v-model="risk" class="form-control my-2" required>
     <option v-for="t of risksTypes" 
            :value="t.id"
            :selected="risk == 0">
     {{ t.title }}
     </option>
    </select>
</div>

<div class="col-md-3 col-sm-12">
    <button type="submit" class="btn btn-primary my-2 px-5">
    Add New Risk
</button>
</div>
</div>
</form>
<div class="modal fade" id="newRisk" tabindex="-1" role="dialog" aria-labelledby="newRiskModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="newRiskModalLabel">
        Add New Risk
        </h5>

        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form v-on:submit.prevent="addRisk()">
      <div class="modal-body">
                  <div class="form-group">
                    <label for="field-title">Title</label>
                      <input v-model.trim="newRisk.title"
                        type="text"
                        class="form-control"
                        id="field-title"
                        placeholder="Enter Risk Title" 
                        required>
                    </div>

                  <div class="form-group">
                    <label for="field-isurer">Isurer</label>
                      <input v-model.trim="newRisk.isurer"
                        type="text"
                        class="form-control"
                        id="field-isurer"
                        placeholder="Enter Insurer name" 
                        required>
                    </div>

                    <!- custom fields goes here -->

                    <div class="form-group" v-for="f of fields">
                      <label :for="f.title">{{ f.title }}</label>
                                            
                      <select v-if="f.widget == 'enum'" 
                             class="form-control"
                             :id="f.title"
                        required>
                        <option v-for="v of f.opts" :value="v.id">
                         {{ v.title }}
                        </option>
                      </select>
                      <input v-else :type="f.widget"
                             class="form-control"
                             :id="f.title"
                             required>

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
<div class="loading bg-success text-white px-4 py-1" v-show="loading">Loading ..</div>
   </main>
    `

}

Vue.component('risks', Risks);
