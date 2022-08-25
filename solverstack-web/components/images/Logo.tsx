import React, { ReactElement } from "react";

// Bootstrap
import Image from "react-bootstrap/Image";

const Logo = (props): ReactElement => {
    return (
        <a href="/">
            <Image 
            src="/logo.png" 
            roundedCircle height={props.height ? props.height : "110px"} />
            </a>
    );
};

export default Logo;
