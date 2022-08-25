import React from "react";

import Profile from "../images/Profile";

interface Props {
    username: string | string[] | undefined;
}

const UserProfile = (props: Props) => {
    return (
        <div>
            <Profile />
            <hr />
            <h5>@{props.username}</h5>
        </div>
    );
};

export default UserProfile;
