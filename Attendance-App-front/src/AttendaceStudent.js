import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';

class AttendanceStudent extends React.Component{
    render(){
        return(
            <div>
       <PersistentDrawerLeft />
       <h1>{this.props.match.params.id}</h1>
            
            </div>
        );
    }
}

export default AttendanceStudent;