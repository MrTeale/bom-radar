# BOM-Radar

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

BOM-Radar generates an restful endpoint via AWS API Gateway that displays the Australian Bureau of Meteorology (BOM)'s Radar for my current location (Brisbane, Australia).

## Built With
[Python 3.6](https://www.python.org/)
[Serverless](https://www.serverless.com/)
[AWS API Gateway](https://aws.amazon.com/api-gateway/)
[AWS Lambda](https://aws.amazon.com/lambda)


## Installation

To install the necessary files to do development on this project, run:

```bash
pip install -r requirements.txt
```

## Deployment

This project is deployed on AWS using Serverless as follows:

```bash
serverless deploy -v
```


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Lachlan Teale - [@mrteale](https://twitter.com/mrteale) - lachlanteale@gmail.com

Project Link: [https://github.com/mrteale/bom-radar](https://github.com/mrteale/bom-radar)

[license-shield]: https://img.shields.io/github/license/mrteale/bom-radar.svg?style=for-the-badge
[license-url]: https://github.com/mrteale/bom-radar/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/mrteale