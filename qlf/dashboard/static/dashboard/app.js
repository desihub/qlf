Ext.onReady(function() {  
  Ext.tip.QuickTipManager.init();

  //-------------- container with bokeh ---------------
  var panelBokeh = {
        title: '<p class="text">QA</p>',
        iconCls: 'x-fa fa-line-chart',
        height: 1024,

        items:[{
        xtype: 'panel',        
        autoScroll: true,
        width: '100%',
            items:[{
                html: '<h2>Spectral signal-to-noise</h2><h3>Calculation of the spectral signal-to-noise  after sky subtraction.</h3>',
                buttonAlign: 'right',
                margin: '10 10 10 10',
                buttons: [{
                     xtype: 'button',
                     formBind: true,
                     itemId: 'btnLogin',
                     text: 'MORE',
                      handler: function(button) {
                        setBokeh(button)
                      },
                }]
            },
            {
                xtype: 'component',
                id: 'qa-snr',
                width: 650,
                text: 'test'
                // height: 650
            }]
        }]
    }
  //-------------- container with bokeh ---------------
  mySourceConfig = {}
  mySource = {}

  // ---------------config xtype -----------------------
  var xtypeConfig = {        
      xtype: 'propertygrid',
      id: 'configproperty',
      me: this,
      scrollable: true,
      myStore: '',
//      config: {
//          mySourceConfig: {},
//          mySource: {}          
//      },
      saveStore: function(){
         Ext.Ajax.request({
              url: "static/ql.json",
              success: function(response) {
                  var obj = Ext.decode(response.responseText);
              
                  console.log(obj)
              }
          });
         console.log('fora', '=', obj)
      },

      
      setConfiguration: function (fields) {
          
          this.store.source = {}
          var me = this,
              sourceConfig = mySourceConfig //me.getMySourceConfig(),
              source =  mySource //me.getSource();


          for (var i = 0; i < fields.length ; i++) {
              var field = fields[i],
                  name = field.name;
              if (field.hasOwnProperty('type')){

                  var type = field.type;

                  switch(type) {
                      case 'select':
                          me.createselect(field);
                          break;
                      case 'multiselect':
                          me.createMultiselect(field);
                          break;
                      case 'text':
                          me.createText(field);
                          break;
                      case 'number':
                          me.createNumber(field);
                          break;
                      case 'date':
                          me.createDate(field);
                          break;
                      default:
                          console.log('default');
                  }


              } else {
                  // Campo automatico só incluir o field no sourceConfig
                  // console.log('teste entrou aqui')
                  sourceConfig[name] = {
                      displayName: field.displayName
                  }
                  if (field.hasOwnProperty('default')) {
                      source[name] = field.default;
                  }
                  else {
                      // a se pensar se e necessario
                      source[name] = '';
                  }
              }
          };
          mySourceConfig = {}
          mySource = {}
          // source = [{ BiasImage: "%%BiasImage"}, {teste: '%%testando' }]
          console.log(source)
          me.setSource(source, sourceConfig);
      },


      createselect: function (field) {
          // console.log('createselect(%o)', field);

          var me = this,
              sourceConfig = mySourceConfig //me.getMySourceConfig(),
              source = mySource //me.getSource(),
              name = field.name,
              options = Array();

          if (field.hasOwnProperty('options')) {            
              var store = Ext.create('Ext.data.Store', {
                  fields: ['value', 'displayName'],
                  data: field['options']
              })

              // criar editor
              var editor = Ext.create('Ext.form.ComboBox', {
                  store: store,                
                  valueField: 'name',
                  displayField: 'name',
                  editable: false
                  // multiSelect: true,                
              });

              // Adicionar o parametro no sourceConfig
              sourceConfig[name] = {
                  displayName: field.displayName,
                  editor: editor
              }          
              

              // ------------------ SOURCE ----------------------
              
              if (field.hasOwnProperty('default')) {                
                  v = store.getAt(store.find('value', field.default));
                  source[name] = v.get('name');
              }
              else {
                  // a se pensar se e necessario
                  source[name] = '';
              }

          }
          else {
              // erro select tem que ter opcoes
          }

      },
      
      createMultiselect: function (field) {
          // console.log('createselect(%o)', field);

          var me = this,
              sourceConfig = mySourceConfig// me.getMySourceConfig(),
              source = mySource //me.getSource(),
              name = field.name,
              options = Array();

          if (field.hasOwnProperty('options')) {            
              var store = Ext.create('Ext.data.Store', {
                  fields: ['value', 'displayName'],
                  data: field['options']
              })

              // criar editor
              var editor = Ext.create('Ext.form.ComboBox', {
                  store: store,                
                  valueField: 'name',
                  displayField: 'name',
                  editable: false,
                  multiSelect: true           
              });

              // Adicionar o parametro no sourceConfig
              sourceConfig[name] = {
                  displayName: field.displayName,
                  editor: editor
              }          
              

              // ------------------ SOURCE ----------------------
              
              if (field.hasOwnProperty('default')) {                
                  v = store.getAt(store.find('value', field.default));
                  source[name] = v.get('name');
              }
              else {
                  // a se pensar se e necessario
                  source[name] = '';
              }

          }
          else {
              // erro select tem que ter opcoes
          }

      },
      createText: function (field) {
          // console.log('createselect(%o)', field);


          var me = this,
              sourceConfig = mySourceConfig // me.getMySourceConfig(),
              source = mySource //me.getSource(),
              name = field.name;
              sourceConfig[name] = {
                  type: 'text'
              }
              source[name] = '';

              

          if (field.hasOwnProperty('default')) {
              source[name] = field.default;
          }
          

      },
      createNumber: function (field) {
          // console.log('createselect(%o)', field);

          var me = this,
              sourceConfig = mySourceConfig//me.getMySourceConfig(),
              source = mySource//me.getSource(),
              name = field.name;
              source[name] = '';
          
         
          sourceConfig[name] = {
                  type: 'number',
                  editable: false
              }
          

          if (field.hasOwnProperty('default')) {
              source[name] = field.default;
          }
          

      },
      createDate: function (field) {
          // console.log('createselect(%o)', field);

          var me = this,
              sourceConfig = mySourceConfig //me.getMySourceConfig(),
              source = mySource //me.getSource(),
              name = field.name;
              source[name] = '';
          
          console.log('field.dateFormat', '=', field.dateFormat)
          
          sourceConfig[name] = {
                  
              editor: Ext.create('Ext.form.field.Date', {selectOnFocus: true}),
              // displayName: 'Start Time'
              dateFormat: 'Y-m-d g:i A'
      
              }        

          if (field.hasOwnProperty('default')) {
              source[name] = field.default;
          }
      }
  }
  
    

  // ---------------config xtype -----------------------


  //--------------- configuration panel ----------------


    var configurationPanel = {
        title: '<p class="text">Configuration</p>',
        iconCls: 'x-fa fa-cog',
        width: 500,
        margin: '10 10 10 10',
        items: [{
            flex: 1,     
            xtype: 'panel',
            defaults: {
                bodyPadding: 10
            },
//            listeners: {
//                afterrender: 'teste'
//            },  
            layout: {
                type: 'hbox',
                pack: 'start'
            },
            items: [{
                flex: 1,
                xtype: 'panel',
                id: 'accordion',
                margin: '0 10 0 0',
                items: [{        
                    xtype: 'panel',
                    layout: 'accordion',                    
                    defaults: {
                        bodyPadding: 10
                    },   

                    items: [],
                    listeners: {
                        afterrender: 
                        function(button) {
                          render(this)
                        }
                    },
                    reference: 'accordion',
                    me: this

                },{
                    xtype: 'button',
                    text: 'Save',
                    margin: '20 10 0 0',
                    handler: function() {
                        // alert('You clicked the button!');
                        console.log(me)
                        panel = me.getView()
                        refs = panel.getReferences()
                        grid = refs.configuration
                        grid.saveStore()

                    }


                }],
                title: ' &nbsp',
                frame: true

            },{
                flex: 1,
                xtype: 'panel',
                id: 'panelgrid',
                items: [xtypeConfig],
                title: ' &nbsp',
                frame: true

            }]
        }]
    }
    

  //--------------- configuration panel ----------------
  var height = window.innerHeight
  //height += - 70 
  //-------------- MAIN PANEL ---------------
  var mainPanel = Ext.create('Ext.tab.Panel', {
    height: height,
    autowidth: true,
    tabPosition: 'left',
    //tabBarHeaderPosition: 0,
    headerPosition: 'top',
    titleRotation:0,
    tabRotation: 0,
    tabBar: {
        border: false
    },

    defaults: {
        bodyPadding: 20,
        textAlign: 'left',
    },
    
    header: {
        title: {

            text: '<h3>Quick Look</h3>',
            margin: '0 0 -15 0',

        },

    },
    items: [
    {
        title: '<p class="text">Home</p>',
        iconCls: 'x-fa fa-home',
        //listeners: {
        //    afterrender: 'teste'
        //}
    },configurationPanel,
    {
        title: '<p class="text">Monitor</p>',
        iconCls: 'x-fa fa-desktop',
        // xtype: 'ccd'
    },
    panelBokeh 
    ],
    renderTo: Ext.getBody(),
  });  
  //-------------- MAIN PANEL ---------------

  //-------------- functions ---------------

  function setBokeh(el){
    Ext.Ajax.request({
      url: '/dashboard/api/qa-snr/',
      success: function(response){
        var obj = Ext.decode(response.responseText);
        console.log(obj)
        if (el.text == 'LESS'){
            document.getElementById("qa-snr").innerHTML = ""
            document.getElementById("qa-snr").style.height = "0px"
            el.setText('MORE')
        }else{
            var imported = document.createElement('script');
            imported.src = obj.src;
            imported.id = obj.id;
            document.getElementById("qa-snr").style.height = "650px"
            document.getElementById("qa-snr").appendChild(imported)
            el.setText('LESS')
        }
      }
    })
  }

  function render(accordionPanel) {
        // exapmple json response
        console.log('here')
        grid = Ext.getCmp('accordion')
        me = this
        Ext.Ajax.request({
            url: "static/ql.json",
            success: function(response) {
                var obj = Ext.decode(response.responseText);
                console.log(obj)
                // obj = Ext.decode(responseText),
                listaAux = []
                listaAuxSteps = []
                lista = []
                function isInArray(value, array) {
                    return array.indexOf(value) > -1;
                }
                console.log(grid)
                grid.setTitle(obj.name)
                for (var i = 0; i < obj['tasks'].length; i++) {
                    // console.log('obj[tasks][i].name ==>(%o)', obj['tasks'][i].name)
                    lista.push(
                        {
                            "title": obj['tasks'][i].name,
                            items: [{
                                xtype: 'fieldcontainer',
                                // layout: 'hbox',
                                items:[
                                    
                                
                                ]
                                }
                            ]
                        }
                    )
                    for (var s = 0; s < obj['tasks'][i].steps.length; s++) {
                        lista[lista.length - 1].items[0].items.push(
                            {
                                xtype     : 'checkboxfield',                                    
                                boxLabel  : obj['tasks'][i].steps[s].name,
                                name      : 'teste',
                                // id        : obj[chave][info][result][step].name,
                                checked   : true,
                                margin: '0 0 0 10'
                            }
                        )
                        configuration = obj['tasks'][i].steps[s].configuration
                        // console.log(typeof configuration)
                        if (typeof configuration !== 'undefined'){
                            lista[lista.length - 1].items[0].items.push(
                                {
                                    xtype: 'button',
                                    iconCls: 'x-fa fa-cog',
                                    tooltip: 'Configuration',
                                    margin: '-28 10 0 200',
                                    padding : '0 0 1 0',
                                    value : {"args": obj['tasks'][i].steps[s].configuration, "StepName" : obj['tasks'][i].name +'('+ obj['tasks'][i].steps[s].name +')'},//obj[chave][info].StepName + '(' + obj[chave][info][result][step].Name + ')'},
                                    handler: function() {
                                        setConfiguration(this.value.args, this.value.StepName)
                                    }

                                }
                            )
                        }
                    };
                };
                // console.log(lista)
                data = lista;
                accordionPanel.add(data);
            }
        })
    }
    function setConfiguration(args, StepName) {
      propertygridConfig = Ext.getCmp('configproperty')
      panelConfig = Ext.getCmp('panelgrid')
      panelConfig.setTitle(StepName);
      cofigArray = Array();
      // console.log("args.length(%o)", args.length);
      if (args.length > 0){
        for (var i = args.length - 1; i >= 0; i--) {
          cofigArray.push(args[i])
          // grid.setSource(args[i]);
          };
      }else{
        propertygridConfig.setSource(args);
      }
        // this.getType(teste)
        // console.log('teste', '=', teste);
      propertygridConfig.setConfiguration(cofigArray);
        // store =  Ext.create('Ext.data.Store', {
        //             fields: ['abbr', 'name'],
        //             data : [
        //                 {"abbr":"AL", "name":"Alabama"},
        //                 {"abbr":"AK", "name":"Alaska"},
        //                 {"abbr":"AZ", "name":"Arizona"}
        //             ]
        //         }),

    }
});