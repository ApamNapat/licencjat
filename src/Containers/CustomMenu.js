import {Menu} from "antd";
import {Link} from "react-router-dom";
import React from "react";

const CustomMenu = (props) => (
    <Menu theme="dark" mode="horizontal">
        <Menu.Item key="1"><Link to="/">Home</Link></Menu.Item>
        {!props.loggedIn && <Menu.Item key="2"><Link to="/register">Register</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="3"><Link to="/settimetable">Set Timetable</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="4"><Link to="/currenttimetable">Your Timetable</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="5"><Link to="/thissemester">This Semester</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="6"><Link to="/abilities">Abilities</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="7"><Link to="/completedcourses">Completed Courses</Link></Menu.Item>}
        {props.loggedIn && <Menu.Item key="8"><Link to="/messages">Messages</Link></Menu.Item>}
        <Menu.Item key="9" style={{'float': 'right'}}><Link to="/about">About</Link></Menu.Item>
        {props.loggedIn &&
        <Menu.Item key="10" onClick={props.processLogout} style={{'float': 'right'}}><Link to="/">Log
            Out</Link></Menu.Item>}
    </Menu>
);

export default CustomMenu;
