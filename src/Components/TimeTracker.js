import React from 'react';

class TimeTracker extends React.Component {
    constructor(props) {
        super(props);
        let date = new Date();
        this.state = {
            hour: date.getUTCHours(),
            minute: date.getUTCMinutes().toString(),
            second: date.getUTCSeconds().toString(),
        };
    }


    componentDidMount = () => {
        this.setState({counter: setInterval(this.clock, 1000)});
    }

    componentWillUnmount = () => {
        clearInterval(this.state.counter);
    }

    clock = () => {
        let date = new Date();
        this.setState({
            hour: date.getUTCHours(),
            minute: date.getUTCMinutes().toString(),
            second: date.getUTCSeconds().toString(),
        });
    }

    render = () => {
        return (
            <p>
                Server Time: {this.state.hour}:{this.state.minute.padStart(2, '0')}:{this.state.second.padStart(2, '0')}
            </p>
        );
    }
}

export default TimeTracker;
