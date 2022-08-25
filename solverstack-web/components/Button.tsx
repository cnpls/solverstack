import React, { useState, useEffect, ReactElement } from "react";
import styled from "styled-components";
import Button from "react-bootstrap/Button";

interface Props {
    type: string | "";
}

const CustomBtn = styled(Button)`
    font-size: 50px;
    color: ${({ theme }) => theme.colors.primary};
`;

const CustomButton = (props: Props): ReactElement => {
    const [data, setData] = useState(null);

    useEffect(() => {
        console.log(data);
    }, [data]);

    const fetchData = async () => {
        let url = "";
        if (props.type === "auth" && process?.env?.userAuth) url = process.env.userAuth;
        else if (props.type === "crud" && process?.env?.userCrud) url = process.env.userCrud;

        const req = await fetch(url);
        const newData = await req.json();
        return setData(newData);
    };

    const handleClick = event => {
        event.preventDefault();
        fetchData();
    };

    return (
        <div>
            <CustomBtn className="my-5" onClick={handleClick}>
                {props.type === "auth" ? "USER AUTH!" : "USER CRUD"}
            </CustomBtn>
        </div>
    );
};

export default CustomButton;
