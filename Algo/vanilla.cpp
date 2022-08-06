

class VanillaOption {
    private:
    void init();
    void copy(const VanillaOption& rhs);

    double K; // strike price
    double r; // interest rate (risk-free)
    double T; // time to maturity
    double S; // Underlying asset price
    double sigma; // volatility

    public:
    VanillaOption();
    VanillaOption(const double & K, const double & r, const double & T, const double & S, const double & sigma); // constructor
    VanillaOption(const VanillaOption& rhs); // copy constructor
    VanillaOption& operator=(const VanillaOption& rhs); // assignment operator
    virtual ~VanillaOption(); // destructor
};