import LocalAuthentication
import Foundation

func waitForBiometricAuthentication() {
    let context = LAContext()
    var error: NSError?

    // Check if biometric authentication is available
    if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
        print("Place your finger on the Touch ID sensor...")

        // Perform biometric authentication
        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Authenticate to proceed") { success, authenticationError in
            if success {
                print("Authentication successful")
                exit(0)  // Exit the Swift program to signal success
            } else {
                print("Authentication failed: \(authenticationError?.localizedDescription ?? "Unknown error")")
                exit(1)  // Exit with failure code
            }
        }
    } else {
        print("Biometric authentication is not available: \(error?.localizedDescription ?? "Unknown error")")
        exit(1)
    }

    // Keep the process alive until the authentication completes
    RunLoop.current.run()
}

waitForBiometricAuthentication()