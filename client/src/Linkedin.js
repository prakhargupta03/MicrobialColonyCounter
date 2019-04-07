import React from "react";
const Linkedin= ({username,profilename,datatype,email})=>{
    return(
        <div>
        <div 
            style={{marginTop:15,marginBottom:15}}
            className="LI-profile-badge"
            data-version="v1" 
            data-size="medium" 
            data-locale="en_US" 
            data-type={datatype} 
            data-theme="light" 
            data-vanity={username}>
            <a className="LI-simple-link" 
                style={{textDecoration:'none',color:'#2B2B52',fontFamily:'roboto',fontSize:25}}
                href={`https://in.linkedin.com/in/${username}?trk=profile-badge`}
            >
                {profilename}
            </a>
        </div>
        <div 
            style={{textAlign:'center',border:'1px solid #ececec',fontFamily:'roboto',padding:2,marginTop:-10}}
            ><b>Email:</b> {email}
        </div>
        </div>
    );
}
export default Linkedin;