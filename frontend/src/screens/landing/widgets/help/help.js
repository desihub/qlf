import React from 'react';
import Paper from '@material-ui/core/Paper';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    maxWidth: '70vw',
    maxHeight: '65vh',
    overflowY: 'auto',
    hyphens: 'auto',
    wordWrap: 'break-word',
    fontSize: 16,
    lineHeight: 1.5,
    fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
    fontWeight: 400,
    margin: '16px',
    padding: '16px',
  },
};

export default class Help extends React.Component {
  render() {
    return (
      <div style={styles.container}>
        <Paper elevation={4} style={styles.main}>
          <h1>About the Quick Look Framework (QLF)</h1>
          <p>
            <span>
              This software is being developed by LIneA in support of the Dark
              Energy Spectroscopic Instrument (DESI), a scientific instrument
              and associated project to make astronomical measurements being
              proposed by the Lawrence Berkeley National Laboratory (LBNL), a
              DOE funded laboratory managed by the University of California at
              Berkeley.
            </span>
          </p>
          <p>
            <span>
              The QLF is part of the Instrument Control System (ICS), which
              performs overall control of the DESI instrument. The QLF provides
              software to process the DESI image data from ICS, based on
              execution of Quick Look pipeline - Quality Assessment results
              (QA). The QLF maintain a database to archive results.
            </span>
          </p>
          <p>
            <b>
              <i>Credits</i>
            </b>
          </p>
          <p>
            <span>
              We would like to thank the contribution of the following LIneA
              team:
            </span>
          </p>
          <ul>
            <li>
              <span>Luiz Nicolaci da Costa (Lead Scientist)</span>
            </li>
            <li>
              <span>Angelo Fausti Neto</span>
            </li>
            <li>
              <span>Carlos Adean</span>
            </li>
            <li>
              <span>Cida Silveira</span>
            </li>
            <li>
              <span>Cristiano Singulani</span>
            </li>
            <li>
              <span>Felipe Machado</span>
            </li>
            <li>
              <span>Felipe Oliveira</span>
            </li>
            <li>
              <span>Maria Luiza Sanchez</span>
            </li>
            <li>
              <span>Ricardo Ogando</span>
            </li>
            <li>
              <span>Riccardo Campisano</span>
            </li>
          </ul>
        </Paper>
      </div>
    );
  }
}
