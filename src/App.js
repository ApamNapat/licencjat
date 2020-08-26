import React from 'react';
import './App.css';

import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
import {Layout} from 'antd';
import axios from 'axios';

import Login from "./Components/Login";
import Status from "./Components/Status";
import TimeTracker from "./Components/TimeTracker";
import CustomMenu from "./Containers/CustomMenu";
import Abilities from "./Components/Abilities";
import TimetableSetter from "./Components/TimetableSetter";
import About from "./Components/About";
import CurrentTimetable from "./Components/CurrentTimetable";
import Register from "./Components/Register";
import ThisSemester from "./Components/ThisSemester";
import CompletedCourses from "./Components/CompletedCourses";
import Messages from "./Components/Messages";
import {notifyOfAPIFailure, urlBase} from "./helpers";

const {Header, Footer, Content} = Layout;
axios.defaults.timeout = 5000


class App extends React.Component {
    constructor(props) {
        super(props);
        let token = localStorage.getItem('token');
        let pk = localStorage.getItem('pk');
        this.state = {
            loggedIn: token !== null,
            token: token,
            pk: pk,
        };
    }

    process_login = (token, pk) => {
        localStorage.setItem('token', token)
        localStorage.setItem('pk', pk)
        this.setState({'token': token, 'loggedIn': true, 'pk': pk});
    };

    processLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('pk');
        this.setState({'token': null, 'loggedIn': false, 'pk': null});
        axios.post(`${urlBase}authentication/logout/`,
            {},
            {'headers': {Authorization: `Token ${this.state.token}`}}
        ).catch(notifyOfAPIFailure);
    };

    render() {
        let paths = this.state.loggedIn ? (
                <Switch>
                    <Route path="/about">
                        <About/>
                    </Route>
                    <Route path="/settimetable">
                        <TimetableSetter pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/currenttimetable">
                        <CurrentTimetable pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/thissemester">
                        <ThisSemester pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/completedcourses">
                        <CompletedCourses pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/messages">
                        <Messages pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/abilities">
                        <Abilities pk={this.state.pk} token={this.state.token}/>
                    </Route>
                    <Route path="/">
                        <Status pk={this.state.pk} token={this.state.token}/>
                    </Route>
                </Switch>)
            : (
                <div>
                    <Switch>
                        <Route path="/about">
                            <About/>
                        </Route>
                        <Route path="/register">
                            <Register loginProcessor={this.process_login}/>
                        </Route>
                        <Route path="/">
                            <Login loginProcessor={this.process_login}/>
                        </Route>
                    </Switch>
                </div>
            )

        return (
            <Router>
                <Layout style={{background: "#E8F4FF"}}>
                    <Header>
                        <CustomMenu loggedIn={this.state.loggedIn} processLogout={this.processLogout}/>
                    </Header>
                    <Content style={{padding: '0 10px', margin: '16px 0'}}>
                        <div>
                            {paths}
                        </div>
                    </Content>
                    <Footer style={{textAlign: 'center', background: "#E8F4FF"}}><TimeTracker/></Footer>
                </Layout>
            </Router>
        );
    }
}


export default App;
