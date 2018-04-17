import React from 'react';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    maxWidth: '600px',
    hyphens: 'auto',
    wordWrap: 'break-word',
    fontSize: 15,
    lineHeight: 1.5,
    fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
    fontWeight: 400,
  },
  link: {
    textDecoration: 'none',
  },
};

export default class AboutUs extends React.Component {
  render() {
    return (
      <div style={styles.container}>
        <div style={styles.main}>
          <h1>About LIneA</h1>
          <p>
            <span>
              The Laboratório Interinstitucional de e-Astronomia (LIneA) was
              created in November 2010 by an agreement signed by three research
              institutes of the Ministry of Science, Technology, Innovation and
              Communication (<a
                style={styles.link}
                href="http://www.mctic.gov.br"
              >
                MCTIC
              </a>) (<a style={styles.link} href="http://www.lncc.br/">
                Laboratório Nacional de Computação Científica
              </a>,{' '}
              <a style={styles.link} href="http://on.br">
                Observatório Nacional
              </a>, &nbsp;e &nbsp;<a
                style={styles.link}
                href="https://www.rnp.br"
              >
                Rede Nacional de Ensino e Pesquisa
              </a>) to provide support for the participation of Brazilian
              scientists in large international programs requiring an IT
              infrastructure such as SDSS, DES, DESI and LSST. Some of its main
              projects include:
            </span>
          </p>
          <ol>
            <li>
              <span>
                The Quick Reduce pipeline available at CTIO to assess the
                quality of the images gathered by DECam;{' '}
              </span>
            </li>
            <li>
              <span>
                The Science Portal, a comprehensive integrated web-based
                end-to-end system to streamline the production of ancillary
                information used to create value-added science ready catalog to
                feed a variety of science analysis workflows;
              </span>
            </li>
            <li>
              <span>
                The Data Server interface available at Fermilab since April 2014
                to enable the visualization of images and objects, and to carry
                out queries in the DESDM database. The interface has been
                accessed 4500 times over the past three years by 250 users;
              </span>
            </li>
            <li>
              <span>
                The Quick Look Framework (QLF) being developed to assess the
                quality of the 15,000 spectra of the 5,000 objects to be
                observed in each exposure of DESI.
              </span>
            </li>
            <li>
              <span>
                The LIneA Science Server being made available at NCSA and which
                will be used as one of the interfaces of the DES data release
                DR1.
              </span>
            </li>
          </ol>
          <p>
            <span>
              In addition, LIneA maintains a data center (1000 cores processing
              cluster, 1 PB mass storage and a host of other machines) for its
              affiliates, currently around 80 members, a mirror site for SDSS
              providing independent SkyServer and CasJobs services, and provides
              support to the computer infrastructure being used by the APOGEE-2
              project at the Las Campanas Observatory.
            </span>
          </p>
        </div>
      </div>
    );
  }
}
