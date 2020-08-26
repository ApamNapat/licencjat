import React from 'react';
import DisplayTemplate from "./DisplayTemplate";
import {urlBase} from "../helpers";

class Ticker extends React.Component {
    constructor(props) {
        super(props);
        console.log(props.seconds)
        this.state = {
            seconds: props.seconds,
        };
    }

    componentDidMount = () => {
        this.setState({counter: setInterval(this.clock, 1000)});
    }

    componentWillUnmount = () => {
        clearInterval(this.state.counter);
    }

    clock = () => {
        const seconds = this.state.seconds;
        this.setState({
            seconds: seconds === 0 ? seconds : seconds - 1,
        });
    }
    render = () => {
        return (
            <>
                Time left: {this.state.seconds}s
            </>
        );
    }
}

class CurrentTimetable extends DisplayTemplate {
    constructor(props) {
        super(props);
        this.url = `${urlBase}timetable/${this.state.pk}/`;
        this.title = "Your Timetable";
    }

    dataProcessor = (data) => {
        return data.map((elem, index) => <>{`${(elem.hour + index) % 24} o'clock: ${elem.action}`}
            <Ticker seconds={Math.floor((new Date(elem.time) - new Date()) / 1000)}/></>);
    }
}

export default CurrentTimetable;