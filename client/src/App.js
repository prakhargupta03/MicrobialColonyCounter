import React, { Component } from 'react';
import './App.css';
import FileUpload from './FileUpload'
import  { post } from 'axios';
import bg from './images/backgroundImage.png';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      image:[],
      text:'',
      output:'',
      count:0
    };
    this.handleFieldChange = this.handleFieldChange.bind(this);
    this.renderFileUpload = this.renderFileUpload.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileUpload = this.fileUpload.bind(this);
  }
  onOpenModal = () => {
    this.setState({ open: true });
  };

  onCloseModal = () => {
    this.setState({ open: false });
  };
  handleFieldChange(fieldId, value) {
    this.setState({image:value});  
  }

  handleEmailChange(event){
    this.setState({email:event.target.value})
  }
  handleWidthChange(event){
    this.setState({width:event.target.value})
  }


  renderFileUpload(k){
    return (
       <FileUpload
            id={k}
            onChange={this.handleFieldChange}
        />      
    )
  }
  handleSubmit(event) {
    //console.log(this.state);
    event.preventDefault();
    this.setState({text:'Processing'})
    this.fileUpload()
    // .then((response)=>{
    //   var formData = response.config.data;
    //   var file
    //   console.log(response)
    //   for(var value of formData.values()) {
    //     console.log('value',value); 
    //     file = value
    //   }
    //   this.setState({
    //     text:'Respose Received',
    //     output: file,
    //     outputfile:URL.createObjectURL(file)
    //   })
    // })
    .then(response => {
      this.setState({
        text:'Respose Received',
        output: response.data.image,
        count:response.data.colonycount
      })
    })
  }

  fileUpload(){
    const url = '/submit';
    const formData = new FormData(); 
    formData.append('photo',this.state.image[0])
    const config = {
        headers: {
            'content-type': 'multipart/form-data',
            'responseType': 'arraybuffer'
        }
    }
    return  post(url, formData,config)
  }

  render() {
    return (
      <div style={{textAlign:'center',background:`url(${bg})`,backgroundSize:'cover',paddingBottom:100,paddingTop:50}}>
        <div style={styles.glowingText}>
            Microbial colony Counter
        </div>        
        <div style={styles.form}>
        {this.renderFileUpload('Upload Image')}
          <br/>
          <br/>
          <form onSubmit={this.handleSubmit} method='post'>
            <button  type="submit" style={styles.button}>
              Submit
            </button>
        </form>
        <br/>
        <span>{this.state.text}</span>
        <br/>
        {this.state.count&&<span>{this.state.count}</span>}
        <br/>
        <br/>
        {this.state.output && <img src={this.state.output} style={{width:300,height:300}} alt = 'output'/>}
        </div>
      </div>
    );
  }
}

const styles = {
  input:{
    border:'none',
    borderBottom:'1px dashed #83A4C5',
    margin:'10px 3px',    
    fontStyle:'italic',
    width:250,
    background:'transparent',
    fontFamily:'roboto',
    fontSize:20,
    color:'#1e1e1e'
  },
  label:{
    fontSize:20,
    fontFamily:'roboto'
  },
  button:{
    padding:'7px 30px',
    fontFamily:'roboto',
    borderRadius:'10px',
    marginLeft:'5px',
    fontSize:15,
    margin:'10px 3px',
    cursor:'pointer',
  },
  form:{
    background:'rgb(255,255,255,0.7)',
    paddingTop:30,
    paddingBottom:30,
    margin:'0 10px',
    borderRadius:10
  },
  glowingText:{
    color:'rgb(99, 54, 38)',
    background: '#333333',
    textShadow:'0 -1px 4px #FFF, 0 -2px 10px #ff0, 0 -10px 20px #ff8000, 0 -18px 40px #F00',
    fontFamily:'roboto',
    fontSize:50,
    margin:30,
    padding:30,
    borderRadius:10
  }
}
export default App;
