import React, { Component } from 'react';
import { FilePond, File, registerPlugin } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';

registerPlugin( FilePondPluginFileValidateType);

class FileUpload extends Component {
  constructor(props){
    super(props);
    this.state={
      files:[]
    }
  }

  handleChange() {
    this.props.onChange(this.props.id,this.state.files);
  }

  render() {
    return (
        <div style={{textAlign:'center',flex: '1',minWidth:'45vw',padding:15}}>
            <h1>{this.props.id}</h1>
            <FilePond ref={ref => this.pond = ref}
                allowMultiple={false}
                acceptedFileTypes={['image/*']}
                onupdatefiles={(fileItems) => {
                // Set current file objects to this.state
                    this.setState({
                        files: fileItems.map(fileItem => fileItem.file)
                    });
                    this.handleChange()                
                }}
                >
                
                {/* Update current files  */}
                {this.state.files.map((file,i) => (
                    <File key={i} src={file} origin="local" />
                ))}
                
            </FilePond>
        </div>
        
    );
  }
}

export default FileUpload;
