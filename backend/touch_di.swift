import Foundation
import Security

func authenticateWithTouchID() -> String {
    let accessControl = SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        .userPresence,
        nil
    )
    
    let attributes: [String: Any] = [
        kSecClass as String: kSecClassKey,
        kSecAttrKeyType as String: kSecAttrKeyTypeEC,
        kSecAttrKeySizeInBits as String: 256,
        kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
        kSecAttrAccessControl as String: accessControl!
    ]
    
    var error: Unmanaged<CFError>?
    guard let privateKey = SecKeyCreateRandomKey(attributes as CFDictionary, &error) else {
        return "Error: \(error!.takeRetainedValue().localizedDescription)"
    }
    
    let context = LAContext()
    context.localizedReason = "Authenticate to generate a key"
    
    var authError: NSError?
    if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &authError) {
        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Authenticate to proceed") { success, error in
            if success {
                print("Authentication successful")
            } else {
                print("Authentication failed")
            }
        }
    } else {
        return "Biometric authentication not available: \(authError?.localizedDescription ?? "Unknown error")"
    }
    
    return "Key created and secured with Touch ID!"
}

print(authenticateWithTouchID())
