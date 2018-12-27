Percent Change
--------------

This is an Alfred Workflow to help you do percentage calculations. You can see
some background info on the original [forum post](http://www.alfredforum.com/topic/4731-percent-change/).

The supported calculations include:

1. *Percent Change* (increase/decrease): `% 3 6` -> 100%
2. *Percentage Of*: 3 is what percent of 100: `% 3 of 100` -> 3%
3. *Percent Of*: 5 percent of 100 is 5: `% 5 percent of 100` -> 5, or `% 5% of 100` -> 5
4. *Percent Decrease*: What is 2 percent from 100: `% 100 - 2%`
5. *Percent Increase*: What is 100 + 2%: `% 100 + 2%`
6. *Original number before Percent Decrease*: What number is 100 2 percent less than?:`% 100 is 2% lt`
7. *Original number before Percent Increase*: What number is 100 2 percent more than?:`% 100 is 2% gt`

## Build:

- Building uses the [workflow-build.py script](https://gist.github.com/AdamWagner/38228953422e830c4484e62ff116466a)
  bundled in this repo.
- To build, run: `python workflow-build.py -f -d . -o .`


## License

This Workflow is available under the terms of the MIT License. See the full
[LICENSE](LICENSE.TXT) for more details.


## Contributing

Contributions to this project are welcome. To contribute, feel free to fork
this repo, add your changes/features/improvements, then open a pull request.
Don't for get to add your name to the [AUTHORS file](AUTHORS.md).
