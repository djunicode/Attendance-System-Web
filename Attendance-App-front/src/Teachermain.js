import React from 'react';
//import Myclasscard from './Components/Myclasscard';
import Ttab from './Components/Ttab';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';

class Teachermain extends React.Component{
    render(){
        return(
        <div>
               <PersistentDrawerLeft /> 

            
            <Ttab />
            {/* <Myclasscard /> */}
            </div>
        );
    }

} 



export default Teachermain;